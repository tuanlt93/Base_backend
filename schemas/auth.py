from pydantic import BaseModel

class TokenLogin(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    access_token: str
    token_type: str = "bearer"