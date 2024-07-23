from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config

# Создаем нашего бота и диспатчер, MemoryStorage хранилище состояний

# Здесь 'my_bot' - это уникальное имя вашего бота, а './locales' - путь к папке с файлами локализации

bot = Bot(token=config('BOT_TOKEN'), parse_mode=ParseMode.HTML)
storage = MemoryStorage()  # use redis
dp = Dispatcher(storage=storage)
