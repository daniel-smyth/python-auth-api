from typing import Literal
from pydantic import BaseModel


class JWTTokenData(BaseModel):
    """The token data found within the JWT authentication token"""

    email: str = None
    permissions: Literal["user", "admin", "super"]
