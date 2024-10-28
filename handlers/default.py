import pandas as pd
from aiogram import types, Router, F
from aiogram.filters import CommandStart, and_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from asgiref.sync import sync_to_async

from data.file_extensions import DocumentTypeFilter
from keyboards import default_kb
from loader import dp, bot
from services.clients_checker.checker import checker_info_from_wb, checker_info_from_ozone
from utils.utils import download_file

default_router = Router(name=__name__)


class ProhibitData:
    # получаем text и контакт для связи
    def __init__(self):
        self.product_name = None


prohibit_data = {}


class FileUploadState(StatesGroup):
    awaiting_file = State()
    market_place = State()


# Создаем функцию для инициализации get_help_text
@sync_to_async
def get_prohibit_text(user_id):
    if user_id not in prohibit_data:
        prohibit_data[user_id] = ProhibitData()
    return prohibit_data[user_id]


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


@dp.message(F.text.in_(['Загрузить файл для WB', 'Загрузить файл для Ozone']))
async def prompt_file_upload(message: types.Message, state: FSMContext):
    market_place = 'WB' if message.text == 'Загрузить файл для WB' else 'Ozone'
    await state.update_data(market_place=market_place)
    await message.answer('Вставьте файл', reply_markup=default_kb.cancel_markup)
    await state.set_state(FileUploadState.awaiting_file)


@default_router.message(
    and_f(FileUploadState.awaiting_file, F.document,
          DocumentTypeFilter(allowed_extensions=['.xlsx', '.xls'])))
async def get_file_excel(message: types.Message, context: dict, state: FSMContext):
    document = message.document
    data = await state.get_data()
    market_place = data.get("market_place")
    await message.answer(f"Файл {document.file_name} получен и обрабатывается.")
    await state.clear()
    # Скачивание файла
    file_stream, error = await download_file(bot, message.document)
    if error:
        await message.answer(error)
        return
    await message.answer('Файл скачен, идёт обработка. Подождите!!')
    # Загрузка данных из файла Excel
    df = pd.read_excel(file_stream, header=4)
    if market_place == 'WB':
        result = await checker_info_from_wb(df=df, context=context, message=message)
    else:
        result = await checker_info_from_ozone(df=df, context=context, message=message)
    await message.answer_document(result)


@dp.message(F.text == 'Добавить запрещёнку')
async def added_prohibit_product(message: types.Message, state: FSMContext):
    await message.answer('В работе..', reply_markup=default_kb.cancel_markup)
    # await state.set_state(ProhibitProductDataState.product_name)


#
#
# @dp.message(ProhibitProductDataState.product_name)
# async def get_product_name(message: types.Message, state: FSMContext):
#     user_id = message.chat.id
#     prohibit_data = await get_prohibit_text(user_id)
#     prohibit_data.product_name = message.text
#     prohibit_data.user_id = message.chat.id
#     await message.answer(text=_(ru_texts['enter_contact_info'], selected_language),
#                          reply_markup=cancel_markup(user_id))
#     await state.set_state(HelpState.contact)
#
#
@dp.message(F.text == 'Список запрещённых товаров')
async def prohibit_product_list(message: types.Message):
    await message.answer('В работе..', reply_markup=default_kb.cancel_markup)
#
# async def save_prohibit_name(product_name, session_maker):
#     """
#     Сохраняем в бд
#     :param product_name:
#     :param session_maker:
#     :return:
#     """
#     country = await ProhibitedProduct.create_country(
#         product_name=product_name,
#         session_maker=session_maker)
#     return country
