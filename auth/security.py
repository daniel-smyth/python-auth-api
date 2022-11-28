import jwt
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "guiyfgc837tgf3iw87-012389764"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def get_password_hash(password: str) -> str:
    """
    Convert a password to an ineligible hash to store in the database

    Args:
        `password`: The password to hash
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against its hashed password to verify a user

    Args:
        `plain_password`: Unhashed password
        `hashed_password`: Hahed password
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    """
    Create an access token for the front end client

    Args:
        - `data`: Token's data (example, permissions)
        - `expires_delta`: When the authentication will expire
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
