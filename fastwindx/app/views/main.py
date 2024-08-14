import logging
from datetime import timedelta

from app.api.deps import get_db
from app.core.config import settings
from app.core.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.db.models.user import User
from app.schemas.user import UserCreate
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status,
)
from fastapi.responses import (
    HTMLResponse,
    RedirectResponse,
)
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

logger = logging.getLogger(__name__)
router = APIRouter()

templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)


@router.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})


@router.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, msg: str = None):
    return templates.TemplateResponse("auth/login.html", {"request": request, "msg": msg})


@router.post("/login")
async def login(request: Request, db: AsyncSession = Depends(get_db)):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")

    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        if request.headers.get("HX-Request") == "true":
            return HTMLResponse('<div class="alert alert-error">Incorrect email or password</div>')
        return templates.TemplateResponse(
            "auth/login.html", {"request": request, "msg": "Incorrect email or password"}
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "id": user.id, "role": user.role},
        expires_delta=access_token_expires,
    )

    response = templates.TemplateResponse("index.html", {"request": request})
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.post("/register", response_class=HTMLResponse)
async def register(request: Request, db: AsyncSession = Depends(get_db)):
    form = await request.form()
    try:
        user = UserCreate(
            username=form.get("username"),
            email=form.get("email"),
            password=form.get("password"),
            first_name=form.get("first_name"),
            last_name=form.get("last_name"),
            role="user",
            phone_number=form.get("phone_number", ""),
        )
    except ValueError as e:
        return templates.TemplateResponse("auth/register.html", {"request": request, "msg": str(e)}, status_code=400)

    result = await db.execute(select(User).where(User.email == user.email))
    if result.scalar_one_or_none():
        return templates.TemplateResponse(
            "auth/register.html",
            {"request": request, "msg": "Email already registered"},
            status_code=400,
        )

    result = await db.execute(select(User).where(User.username == user.username))
    if result.scalar_one_or_none():
        return templates.TemplateResponse(
            "auth/register.html",
            {"request": request, "msg": "Username already taken"},
            status_code=400,
        )

    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        phone_number=user.phone_number,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "id": db_user.id, "role": db_user.role},
        expires_delta=access_token_expires,
    )

    response = RedirectResponse(url="/login?msg=User successfully created", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response


@router.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/login?msg=Logout Successful", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("access_token")
    return response
