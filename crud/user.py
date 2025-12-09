from http.client import HTTPException
from sqlalchemy import select
from core import jwt_sec, db
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserCreate
from db_models.models import User
from utils.logger import Logger
from fastapi import Depends, HTTPException

async def create_user(session: AsyncSession, data: UserCreate):
    user = User(
        email=data.email,
        full_name=data.full_name,
        hashed_password=jwt_sec.hash_password(data.password),
        role_id=data.role_id
    )
    if data.role_id == 0:
        raise HTTPException(403, "Permission denied")
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def create_manufacturer():
    user = User(
        email="demo@gmail.com",
        full_name="Maunufacturer",
        hashed_password=jwt_sec.hash_password("demo1234"),
        role_id=0  # manufacturer role_id
    )
    session = await db.get_session()
    
    existing_user = await read_user_by_email(session, user.email)
    if existing_user:
        await session.close()
        return 
    
    Logger().info("Creating default manufacturer user...")
    
    try:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    finally:
        await session.close()

async def read_user_by_email(session: AsyncSession, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()