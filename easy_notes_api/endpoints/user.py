from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from easy_notes_api.schemas import RegistrationForm
from easy_notes_api.db.connection import get_session
from easy_notes_api.utils.user import (
    register_user,
    authenticate_user,
    create_access_token,
    get_current_user
)
from easy_notes_api.schemas import RegistrationSuccess, Token, UserSchema
from easy_notes_api.config import get_settings, DefaultSettings
from easy_notes_api.db.models import User


api_router = APIRouter(prefix="/user", tags=["User"])


@api_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,    
    response_model=RegistrationSuccess,
)
async def registration(
    registration_form: Annotated[RegistrationForm, Body()],
    session: AsyncSession = Depends(get_session),
):
    is_success = await register_user(session, registration_form)
    if is_success:
        return {"message": "Registered!"}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Username already exists.",
    )


@api_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
    settings: Annotated[DefaultSettings, Depends(get_settings)]
) -> Token:
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@api_router.get("/users/me/", response_model=UserSchema)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user