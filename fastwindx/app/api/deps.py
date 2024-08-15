from typing import AsyncGenerator, Optional, cast

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.engine.result import Row  # type: ignore[attr-defined]
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.security import ALGORITHM, SECRET_KEY, oauth2_scheme
from app.db.base import get_session
from app.db.models.user import User
from app.schemas.user import TokenData


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with get_session() as session:
        yield session


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as err:
        raise credentials_exception from err

    result = await db.execute(select(User).where(User.email == token_data.username))
    user = result.first()
    if user is None:
        raise credentials_exception

    # Safely extract User object from the result
    if isinstance(user, tuple):
        return cast(User, user[0])
    elif isinstance(user, Row):
        return cast(User, user[0])
    else:
        return cast(User, user)
