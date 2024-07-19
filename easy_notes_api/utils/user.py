from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from sqlalchemy import exc, select
from sqlalchemy.ext.asyncio import AsyncSession

from easy_notes_api.config import DefaultSettings, get_settings
from easy_notes_api.db.connection import get_session
from easy_notes_api.db.models import User
from easy_notes_api.schemas import RegistrationForm, TokenData


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return get_settings().PWD_CONTEXT.verify(plain_password, hashed_password)


async def get_user(session: AsyncSession, username: str) -> User | None:
    query = select(User).where(User.username == username)
    return await session.scalar(query)


async def register_user(session: AsyncSession, user_data: RegistrationForm) -> bool:
    user = User(**user_data.model_dump(exclude_unset=True))
    session.add(user)
    try:
        await session.commit()
    except exc.IntegrityError:
        return False
    return True


async def authenticate_user(session: AsyncSession, username: str, password: str):
    user = await get_user(session, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    settings = get_settings()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(get_settings().OAUTH2_SCHEME)],
    session: Annotated[AsyncSession, Depends(get_session)],
    settings: Annotated[DefaultSettings, Depends(get_settings)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(session, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
