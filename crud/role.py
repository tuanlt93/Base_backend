from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from db_models.models import Role
from core import db
from utils.logger import Logger

async def create_role(name: str, role_id: int) -> Role:
    role = Role(
        name=name,
        role_id=role_id
    )

    session = await db.get_session()
    try:
        session.add(role)
        await session.commit()
        await session.refresh(role)
        return role
    finally:
        await session.close()

async def create_roles():
    default_roles : list[dict[str, int]] = [
        {"name": "manufacturer", "role_id": 0},
        {"name": "admin", "role_id": 1},
        {"name": "user", "role_id": 2},
    ]

    def normalize(roles):
        return sorted(roles, key=lambda r: r["role_id"])

    db_roles = normalize(await read_all_roles())
    expected_roles = normalize(default_roles)

    if db_roles == expected_roles:
        return
    
    Logger().info("Creating default roles...")
    await delete_all_role()
    
    for r in default_roles:
        await create_role(r["name"], r["role_id"])


async def read_all_roles() -> list:
    session = await db.get_session()
    try:
        result = await session.execute(select(Role))
        roles = result.scalars().all()
        return [
            {"name": r.name, "role_id": r.role_id}
            for r in roles
        ]
    finally:
        await session.close()

async def delete_all_role():
    session = await db.get_session()
    try:
        await session.execute(delete(Role))
        await session.commit()
    finally:
        await session.close()
