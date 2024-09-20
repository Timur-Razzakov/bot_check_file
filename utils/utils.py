import io

import pandas
from aiogram import Bot
from aiogram.types import Document


async def download_file(bot: Bot, document: Document) -> tuple[io.BytesIO, str | None]:
    """
    Функция для скачивания файла из тг.
    """
    error = None
    file_info = await bot.get_file(document.file_id)
    file_stream = io.BytesIO()

    await bot.download_file(file_info.file_path, file_stream)
    file_stream.seek(0)

    # Проверка, что файл был скачан правильно
    if file_stream.getbuffer().nbytes == 0:
        error = "Ошибка: файл не был скачан."

    return file_stream, error


def is_convertible_to_int(value):
    if pandas.isna(value):
        return True
    try:
        # Пробуем преобразовать значение в int
        int(value)
        return True
    except ValueError:
        return False
