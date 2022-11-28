import jwt
from fastapi import Depends, HTTPException, status

from models.security import JWTTokenData
from models.user import User

import database.user as db

import auth.security


async def authenticate_user(email: str, password: str):
    """
    Authenticate that a user has provided the correct password when
    logging in

    Args:
        - `email`: The email to authenticate
        - `password`: The password to authenticate
    """
    user = await db.get_user_by_email(email)

    if not user:
        return False

    if not auth.security.verify_password(password, user.hashed_password):
        return False

    return user


async def get_current_user_from_token(
    token: str = Depends(auth.security.oauth2_scheme),
):
    """
    Get the current active user from the client's OAuth2 token. Required for
    authenication. Returns the active user from the database

    Args:
        - `token`: OAuth2 token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            auth.security.SECRET_KEY,
            algorithms=[auth.security.ALGORITHM],
        )

        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception

        permissions: str = payload.get("permissions")
        token_data = JWTTokenData(email=email, permissions=permissions)

    except jwt.PyJWTError:
        raise credentials_exception

    user = await db.get_user_by_email(token_data.email)

    if user is None:
        raise credentials_exception

    return user


async def get_active_user(
    current_user: User = Depends(get_current_user_from_token),
):
    """
    Get the current user from OAuth token and return the user
    if "is_active"

    Args:
        - `current_user`: The current OAuth user
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


async def get_current_active_admin(
    current_user: User = Depends(get_current_user_from_token),
):
    """
    Get the current user from OAuth token and return the user
    if "is_active" and "is_admin_user"

    Args:
        - `current_user`: The current OAuth user
    """
    if not current_user.is_admin_user:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )

    return current_user


async def get_current_active_superuser(
    current_user: User = Depends(get_current_user_from_token),
):
    """
    Get the current user from OAuth token and return the user
    if "is_active" and "is_super_user"

    Args:
        - `current_user`: The current OAuth user
    """
    if not current_user.is_super_user:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )

    return current_user
