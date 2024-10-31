from typing import Union

from decouple import config
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine as _create_async_engine
from sqlalchemy.orm import sessionmaker


# Echo отвечает за вывод всех действий
# для работы с бд
# pool_pre_ping отвечает за тестиврование соединения с бд
def create_async_engine(url: Union[str, URL], ) -> AsyncEngine:
    return _create_async_engine(url=url, echo=bool(config('DEBUG')), pool_pre_ping=True)


# создаёт все схемы в бд если исп alembic, то не нужно исп это
async def proceed_schemas(engine: AsyncEngine, metadata) -> None:
    """

     :param engine:
     :param metadata:
     """
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)


# Engine отвечает за непосредственно соединение с бд
# session-maker отвечает за создание и манипуляции с сессиями записи/чтение к бд
def get_session_maker(engine) -> sessionmaker:  # expire_on_commit - чтобы сессия не истекала при коммите
    async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return async_session_maker
