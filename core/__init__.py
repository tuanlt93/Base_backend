from .database.sqlite import SqliteDB
from .security.jwt_sec import JWTSecurity
from .mq.redis_mq import RedisMQ
from .tasks.bachgroud_tasks import BackgroundTasks

db = SqliteDB()
jwt_sec = JWTSecurity()
mq = RedisMQ()
bt = BackgroundTasks
