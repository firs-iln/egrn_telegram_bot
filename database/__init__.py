from sqlalchemy.ext.asyncio import create_async_engine
from config import config

engine = create_async_engine(
    config.DB_URI.get_secret_value(),
    echo=True,
)
