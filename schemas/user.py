from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    """
    email: EmailStr,
    full_name: str | None,
    password: str,
    role_id: int,
    """
    email: EmailStr
    full_name: str | None
    password: str
    role_id: int

class UserOut(BaseModel):
    """
    id: int,
    email: EmailStr,
    full_name: str | None,
    role_id: int,
    """
    id: int
    email: EmailStr
    full_name: str | None
    is_active: bool
    role_id: int

    class Config:
        from_attributes = True