from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from .base_db import BaseDB
from config import DATABASE_URL


class SqliteDB(BaseDB):
    def __init__(self):
        self.__engine = create_async_engine(
            DATABASE_URL,
            echo = False,
            future = True,
            connect_args = {"check_same_thread": False},
        )

        # Tạo SessionFactory
        self.__sessionLocal = async_sessionmaker(
            bind = self.__engine,
            expire_on_commit = False
        )

        self.__base = declarative_base()


    @property
    def Base(self):
        return self.__base

    # ----------------------------
    # DB Init
    # ----------------------------
    async def start_db(self):
        async with self.__engine.begin() as conn:
            await conn.run_sync(self.__base.metadata.create_all)

    async def stop_db(self):
        await self.__engine.dispose()

    # ----------------------------
    # FastAPI dependency (async generator)
    # ----------------------------
    async def get_write_session(self):
        """Generator trả về session để ghi."""
        async with self.__sessionLocal() as session:
            yield session

    async def get_read_session(self):
        """Generator trả về session để đọc."""
        async with self.__sessionLocal() as session:
            yield session


    # ----------------------------
    # Helper dùng ngoài FastAPI (test script)
    # ----------------------------
    async def get_session(self) -> AsyncSession:
        """LẤY SESSION THẬT (không phải generator)."""
        return self.__sessionLocal()