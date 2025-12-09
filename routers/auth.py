from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core import db
from core import jwt_sec
from schemas.auth import TokenLogin, TokenRefresh
from sqlalchemy import select
from db_models.models import User

router = APIRouter()

@router.post("/login", response_model=TokenLogin)
async def login(email: str, password: str, session: AsyncSession = Depends(db.get_read_session)):

    rs = await session.execute(select(User).where(User.email == email))
    user = rs.scalar_one_or_none()

    if not jwt_sec.verify_password(password, user.hashed_password):
        user = None
    if not user:
        raise HTTPException(400, "Invalid credentials")

    return TokenLogin(
        access_token=jwt_sec.create_access_token(user.email),
        refresh_token=jwt_sec.create_refresh_token(user.email),
    )

@router.post("/refresh", response_model=TokenRefresh)
async def refresh_token(refresh_token: str):
    try:
        payload = jwt_sec.decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise Exception("Not refresh token")
    except Exception:
        raise HTTPException(401, "Invalid refresh token")

    email = payload["sub"]
    return TokenRefresh(
        access_token=jwt_sec.create_access_token(email),
    )
