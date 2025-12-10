from .cache.redis_cache import RedisCache
from .database.sqlite import SqliteDB
from .security.jwt_sec import JWTSecurity
from .mq.redis_mq import RedisMQ
from .tasks.bachgroud_tasks import BackgroundTasks

cache = RedisCache()
db = SqliteDB()
jwt_sec = JWTSecurity()
mq = RedisMQ(cache)
bt = BackgroundTasks
