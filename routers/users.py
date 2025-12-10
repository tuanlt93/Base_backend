from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.ext.asyncio import AsyncSession
from core import db
from schemas.user import UserCreate, UserOut
import crud.user as crud_user
from routers.utils import require_role
from sqlalchemy import select
from db_models.models import User

router = APIRouter()

@router.post("", response_model=UserOut)
async def create_user(
    data: UserCreate,
    session: AsyncSession = Depends(db.get_write_session),
    _=Depends(require_role("manufacturer", "admin"))
):

    rs = await session.execute(select(User).where(User.email == data.email))
    exist = rs.scalar_one_or_none()
    if exist:
        raise HTTPException(400, "Email exists")
    return await crud_user.create_user(session, data)

@router.get("/accounts", response_model= list[UserOut])
async def get_accounts(
    session: AsyncSession = Depends(db.get_read_session),
    _=Depends(require_role("manufacturer", "admin"))
):
    users = await crud_user.get_users(session)
    return users