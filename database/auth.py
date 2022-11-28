from datetime import timedelta
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

import auth.jwt as jwt
import auth.security as security

import models.user as models
import database.user as db


async def login_user(form_data: OAuth2PasswordRequestForm):
    user: models.User = await jwt.authenticate_user(
        form_data.username, form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.is_super_user:
        permissions = "super"
    elif user.is_admin_user:
        permissions = "admin"
    else:
        permissions = "user"

    access_token_expires = timedelta(
        minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    access_token = security.create_access_token(
        data={
            "sub": user.email,
            "permissions": permissions,
        },
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


async def signup_user(form_data: OAuth2PasswordRequestForm):
    user = await db.get_user_by_email(form_data.username)

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )

    new_user = await db.create_user(
        models.UserCreate(
            email=form_data.username,
            password=form_data.password,
            is_active=True,
            is_super_user=True,
            is_admin=True,
        ),
    )

    access_token_expires = timedelta(
        minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    if new_user.is_super_user:
        permissions = "super"
    elif new_user.is_admin_user:
        permissions = "admin"
    else:
        permissions = "user"

    access_token = security.create_access_token(
        data={"sub": new_user.email, "permissions": permissions},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}
