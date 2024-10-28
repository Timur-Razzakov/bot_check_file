from aiogram.fsm.state import StatesGroup, State


# Машина состояний для отправки данных
class ProhibitProductDataState(StatesGroup):
    product_name = State()

class FileUploadState(StatesGroup):
    awaiting_file = State()
    market_place = State()
