from datetime import timedelta
from typing import List

from app.api.deps import get_current_user, get_db
from app.core.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_password_hash, verify_password
from app.db.models.user import User as DBUser
from app.schemas.user import Token, User, UserCreate
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

router = APIRouter()


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)) -> Token:
    db_user = db.exec(select(DBUser).where(DBUser.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = db.exec(select(DBUser).where(DBUser.username == user.username)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_password = get_password_hash(user.password)
    db_user = DBUser(
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_password,
        role=user.role,
        phone_number=user.phone_number,
        is_active=True,  # assuming new users are active by default
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "id": db_user.id, "role": db_user.role},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    user = db.exec(select(DBUser).where(DBUser.email == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "id": user.id, "role": user.role},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=User)
async def read_users_me(current_user: DBUser = Depends(get_current_user)) -> User:
    return User.from_orm(current_user)


@router.put("/me", response_model=User)
async def update_user_me(
    user_update: UserCreate,
    current_user: DBUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    if user_update.email != current_user.email:
        if db.exec(select(DBUser).where(DBUser.email == user_update.email)).first():
            raise HTTPException(status_code=400, detail="Email already registered")

    if user_update.username != current_user.username:
        if db.exec(select(DBUser).where(DBUser.username == user_update.username)).first():
            raise HTTPException(status_code=400, detail="Username already taken")

    current_user.email = user_update.email
    current_user.username = user_update.username
    current_user.first_name = user_update.first_name
    current_user.last_name = user_update.last_name
    current_user.role = user_update.role
    current_user.phone_number = user_update.phone_number

    if user_update.password:
        current_user.hashed_password = get_password_hash(user_update.password)

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return User.from_orm(current_user)


@router.get("/users", response_model=List[User])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: DBUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[User]:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    users = db.exec(select(DBUser).offset(skip).limit(limit)).all()
    return [User.from_orm(user) for user in users]


@router.get("/users/{user_id}", response_model=User)
async def read_user(
    user_id: int, current_user: DBUser = Depends(get_current_user), db: Session = Depends(get_db)
) -> User:
    user = db.get(DBUser, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return User.from_orm(user)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int, current_user: DBUser = Depends(get_current_user), db: Session = Depends(get_db)
) -> None:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    user = db.get(DBUser, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
