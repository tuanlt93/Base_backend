from fastapi import FastAPI
from contextlib import asynccontextmanager
from core import db, cache
from crud.role import create_roles
from crud.user import create_manufacturer
import asyncio
from routers import auth, users
from utils.logger import Logger

async def on_msg(msg: str):
    print("New message:", msg)
    await asyncio.sleep(2)  # non-blocking
    print("New message: -----", msg)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup database
    await db.start_db()
    
    # Create roles if not exist
    await create_roles()
    
    # Create default manufacturer user if not exist
    await create_manufacturer()

    await cache.connect()

    # bg_tasks = bt(app)
    # await mq.connect()

    # tasks: dict[str, callable] = {}
    # tasks["task1"] = mq.subscriber("test_topic", on_msg)
    # tasks["task2"] = mq.subscriber("test_topic_2", on_msg)

    # bg_tasks.start_tasks(tasks)



    yield    # BẮT BUỘC

    print(">>> Shutdown")
    await db.stop_db()
    await cache.disconnect()
    # bg_tasks.stop_tasks()

    # await mq.disconnect()


Logger(level='warn', to_screen=True, to_file=False)
app = FastAPI(lifespan=lifespan)


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
