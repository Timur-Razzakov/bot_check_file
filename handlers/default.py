import io

import pandas as pd
from aiogram import types, Router, F
from aiogram.filters import CommandStart, and_f
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from openpyxl.reader.excel import load_workbook

from data.file_extensions import DocumentTypeFilter, is_valid_passport, yellow_fill, is_valid_pinfl
from keyboards import default_kb
from loader import dp, bot

default_router = Router(name=__name__)


@dp.message(
    lambda message: message.text == 'Отмена')
async def cmd_cancel(message: types.Message, state: FSMContext):
    """Отмена"""
    current_state = await state.get_state()
    if current_state:
        await state.clear()

    await message.answer(text='Выберите из списка', reply_markup=default_kb.menu)


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer('Здравствуйте. Выберите из списка',
                         reply_markup=default_kb.menu)


@dp.message(F.text == 'Загрузить файл')
async def prompt_file_upload(message: types.Message):
    await message.answer('Вставьте файл', reply_markup=default_kb.cancel_markup)


@default_router.message(and_f(F.document, DocumentTypeFilter(allowed_extensions=['.xlsx', '.xls'])))
async def get_file_excel(message: types.Message):
    # Скачивание файла
    document = message.document
    file_name = document.file_name
    file_info = await bot.get_file(document.file_id)
    file_stream = io.BytesIO()
    await bot.download_file(file_info.file_path, file_stream)
    file_stream.seek(0)

    # Проверка, что файл был скачан правильно
    if file_stream.getbuffer().nbytes == 0:
        await message.answer("Ошибка: файл не был скачан.")
        return

    # Загрузка данных из файла Excel
    df = pd.read_excel(file_stream, header=4, skiprows=[5])

    # Загрузка рабочего листа Excel
    file_stream.seek(0)  # Сброс позиции потока для openpyxl
    workbook = load_workbook(file_stream)
    sheet = workbook.active

    passport_col_idx = df.columns.get_loc('Номер паспорта') + 1
    pinfl_col_idx = df.columns.get_loc('Пинфл') + 1

    for index, row in df.iterrows():
        passport = str(row.get('Номер паспорта', ''))
        pinfl = str(row.get('Пинфл', ''))
        # Проверка на отсутствие или некорректность данных
        if not is_valid_passport(passport):
            cell = sheet.cell(row=index + 7, column=passport_col_idx)
            cell.fill = yellow_fill
        if not is_valid_pinfl(pinfl):
            cell = sheet.cell(row=index + 7, column=pinfl_col_idx)
            cell.fill = yellow_fill

    # Сохранение изменений в новый файл Excel в память
    output_stream = io.BytesIO()
    workbook.save(output_stream)
    output_stream.seek(0)
    # Отправка изменённого файла пользователю
    # await message.answer_document(types.InputFile(output_stream, filename=f'colored_{file_name}'))
    file = BufferedInputFile(output_stream.getvalue(), "output.xlsx")
    await message.answer_document(file)
