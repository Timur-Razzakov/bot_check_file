import os

from aiogram import types
from aiogram.filters import BaseFilter
from openpyxl.styles import PatternFill

# Задаем цвета для окрашивания
red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")
yellow_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
blue_fill = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")

# Путь к папке для загрузок
DOWNLOADS_DIR = 'downloads'
if not os.path.exists(DOWNLOADS_DIR):
    os.makedirs(DOWNLOADS_DIR)


class DocumentTypeFilter(BaseFilter):
    def __init__(self, allowed_extensions: list = None):
        self.allowed_extensions = ['.xlsx', '.xls'] if not allowed_extensions else allowed_extensions

    async def __call__(self, message: types.Message) -> bool:
        if message.document:
            file_extension = os.path.splitext(message.document.file_name)[1].lower()
            if file_extension in self.allowed_extensions:
                return True

        await message.answer("Неправильное расширение файла. Доступные форматы: "
                             f"<b>{', '.join(self.allowed_extensions)}</b>")
        return False


def process_excel_file(file_path: str):
    # Здесь должна быть логика для обработки Excel файла
    # Например, можно использовать библиотеку pandas для чтения и обработки файла
    import pandas as pd

    df = pd.read_excel(file_path)
    # Выполните необходимые операции с данными
    print(df.head())

    # Не забудьте удалить файл после обработки, если он больше не нужен
    os.remove(file_path)


# Функция для проверки корректности номера паспорта
def is_valid_passport(passport):
    passport = passport.strip()
    result = isinstance(passport, str) and len(passport) == 9 and passport[:2].isalpha() and passport[
                                                                                             2:].isdigit()
    return result


def is_valid_pinfl(pinfl):
    pinfl = pinfl.strip()
    result = pinfl.isdigit() and len(pinfl) == 14
    return result
