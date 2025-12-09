from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core import jwt_sec, db
from db_models.models import User
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

oauth = HTTPBearer()

async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(oauth),
    session: AsyncSession = Depends(db.get_read_session)
):
    payload = jwt_sec.decode_token(token.credentials)
    email = payload["sub"]

    stmt = (
        select(User)
        .options(selectinload(User.role))   # ⭐ Load luôn role
        .where(User.email == email)
    )
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

def require_role(*role_name: str):
    async def role_checker(user: User = Depends(get_current_user)):
        if user.role.name not in role_name:
            raise HTTPException(403, "Permission denied")
        return user

    return role_checker
