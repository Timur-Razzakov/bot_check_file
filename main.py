import asyncio
import logging
import sys

from aiogram.types import BotCommand
from sqlalchemy import URL

from data import config
from handlers import bot_commands
from handlers.default import default_router
from loader import dp, bot
from services.auth.auth import get_access_token
from utils.db import create_async_engine, Base, get_session_maker, proceed_schemas


async def main() -> None:
    # Проверяем авторизацию на сайте ВБ без этого запускать бота бессмысленно
    token, error = await get_access_token(
        employee_id=config.WB_EMPLOYEE_ID, password=config.WB_PASSWORD
    )
    if error:
        logging.error(error)
        logging.error("Возникла ошибка при авторизации обратитесь разработчику")
        return

    # создаём боковую панель
    commands_for_bot = []
    for cmd in bot_commands:  # импортируем из handlers/init
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))
    await bot.set_my_commands(commands=commands_for_bot)
    dp.include_router(default_router)

    # подключаемся к бд
    postgresql_url = URL.create(
        'postgresql+asyncpg',
        username=config.DB_USER,
        password=config.DB_PASS,
        database=config.DB_NAME,
        host=config.DB_HOST,
        port=config.DB_PORT
    )
    async_engine = create_async_engine(postgresql_url)
    session_maker = get_session_maker(async_engine)  # для работы с бд создаём сессии
    await proceed_schemas(async_engine, Base.metadata)
    await async_engine.dispose()  # решает проблему с event loop
    await dp.start_polling(bot, session_maker=session_maker, skip_updates=True, context={"access_token": token})


if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
