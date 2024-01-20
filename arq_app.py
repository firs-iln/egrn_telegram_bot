from arq import create_pool
from arq.connections import RedisSettings
from arq.worker import ArqRedis

from tasks.check_egrn_request_status import check_egrn_request_status

from config import config

redis_settings = RedisSettings(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    database=config.REDIS_DB,
)


async def init_arq_pool() -> ArqRedis:
    arq_pool = await create_pool(redis_settings)
    return arq_pool


class WorkerSettings:
    functions = [
        check_egrn_request_status,
    ]
    redis_settings = redis_settings
