from http.client import HTTPException
import json
from sqlalchemy import select
from core import jwt_sec, db, cache
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserCreate
from db_models.models import User
from utils.logger import Logger
from fastapi import Depends, HTTPException

CACHE_KEY_USERS = "users:list:v1"
CACHE_EXPIRE = 60  # 60 seconds (1 phút)

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
    await cache.delete(CACHE_KEY_USERS)
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

async def get_users(session: AsyncSession) -> list[User]:
    cached = await cache.get(CACHE_KEY_USERS)
    if cached:
        return cached
    
    stmt = (
        select(User)
        .where(User.role_id != 0)   # lọc ngay trong DB
        .order_by(User.id.asc())
    )
    result = await session.execute(stmt)
    users = result.scalars().all()
    users_dict = [
        {"id": u.id, "email": u.email, "full_name": u.full_name, "is_active": u.is_active, "role_id": u.role_id}
        for u in users
    ]

    await cache.set(CACHE_KEY_USERS, users_dict)
    return users_dict
