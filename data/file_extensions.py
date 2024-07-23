import os

from aiogram import types
from aiogram.filters import BaseFilter
from openpyxl.styles import PatternFill

from data.prohibit_product import PROHIBIT_PRODUCT

# Задаем цвета для окрашивания
red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")
yellow_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
blue_fill = PatternFill(start_color="00B0F0", end_color="00B0F0", fill_type="solid")
violet_fill = PatternFill(start_color="8B00FF", end_color="8B00FF", fill_type="solid")

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


# Функция для проверки корректности номера паспорта
def is_valid_passport(passport):
    passport = passport.strip()
    result = isinstance(passport, str) and len(passport) == 9 and passport[:2].isalpha() and passport[
                                                                                             2:].isdigit()
    return result


def is_valid_pinfl(pinfl):
    pinfl = pinfl.strip()
    try:
        pinfl = int(float(pinfl))
    except Exception as e:
        return False
    return len(str(pinfl)) == 14


def is_phone_word_validator(value: str) -> bool:
    return 'телефон' in value.lower() or 'смартфон' in value.lower()


def contains_prohibited_product(text):
    """Функция для проверки наличия запрещённого товара в тексте."""
    for product in PROHIBIT_PRODUCT:
        if product.lower() in text.lower():
            return True
    return False
