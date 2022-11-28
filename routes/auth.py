from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

import database.auth as db

r = APIRouter(
    tags=["Authentication Routes"],
    prefix="/auth",
)


@r.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Log in a user and return a client access token containing the user's
    permissions

    Args:
        - `form_data`: The form data containing user details
    """
    access_token = await db.login_user(form_data)

    return access_token


@r.post("/signup")
async def signup(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Sign up a user and return a client access token containing the user's
    permissions

    Args:
        - `form_data`: The form data containing user details
    """
    access_token = await db.signup_user(form_data)

    return access_token
