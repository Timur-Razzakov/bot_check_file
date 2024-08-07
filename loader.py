from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config

# Создаем нашего бота и диспатчер, MemoryStorage хранилище состояний

# Здесь 'my_bot' - это уникальное имя вашего бота, а './locales' - путь к папке с файлами локализации
# Установка кастомных значений для таймаутов
# timeout = aiohttp.ClientTimeout(
#     total=None,  # Общее время ожидания не ограничено
#     connect=10,  # Время ожидания подключения
#     sock_connect=10,  # Время ожидания установки соединения
#     sock_read=10  # Время ожидания чтения сокета
# )
#
# # Создание кастомной сессии
# session = AiohttpSession(timeout=timeout)
bot = Bot(token=config('BOT_TOKEN'), parse_mode=ParseMode.HTML)
storage = MemoryStorage()  # use redis
dp = Dispatcher(storage=storage)
