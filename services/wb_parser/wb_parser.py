import asyncio
from collections import defaultdict, OrderedDict

import aiohttp
import pandas
from aiogram.types import Message

from data.config import WB_EMPLOYEE_ID, WB_PASSWORD
from services.auth.auth import check_token, login
from services.wb.wb_api import get_products_by_shk_id, get_products_full_info

MAX_CONCURRENT_REQUESTS = 50


async def get_shk_info(session, semaphore, token, shk, empties_products_shk, sku_shk_dict):
    async with semaphore:
        sku_id = await get_products_by_shk_id(session, token, shk)
        if sku_id:
            sku_shk_dict[str(sku_id)].append(shk)
        else:
            empties_products_shk.append(shk)


async def get_sku_info(session, semaphore, token, sku_ids, skus_full_info, message, counter, max_length):
    async with semaphore:
        skus_full_info.extend(await get_products_full_info(session=session, token=token, sku_ids=sku_ids))
        async with counter["lock"]:
            counter["count"] += len(sku_ids)
            await message.answer(f"Обработано {counter['count']} из {max_length}")


async def get_metadata_from_wb(message: Message, shk_dict: OrderedDict, token: str) -> tuple[pandas.DataFrame, str]:
    await message.reply(f"Обнаружено {len(shk_dict)} штрих-кодов.")
    await message.answer("Авторизация...")
    if not await check_token(token):
        token, error = await login(employee_id=WB_EMPLOYEE_ID, password=WB_PASSWORD)
        if error:
            await message.answer("Возникла ошибка при авторизации обратитесь разработчику")
            await message.answer(f"Текст ошибки: \n\n {error}")

    await message.answer("Начало загрузки данных из WB...")

    skus_full_info = []
    empties_products_shk = []
    sku_shk_dict = defaultdict(list)

    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    async with aiohttp.ClientSession() as session:
        tasks = [
            get_shk_info(session, semaphore, token, shk, empties_products_shk, sku_shk_dict)
            for shk in list(shk_dict.keys())
        ]
        await asyncio.gather(*tasks)

    exists_products_sku = [int(sku_id) for sku_id in sku_shk_dict.keys()]
    await message.answer("Информация о штрих-кодах подгружено из WB.")
    await message.answer("Идёт обработка...")
    async with aiohttp.ClientSession() as session:
        step = 1000
        chunks = []
        counter = {"count": 0, "lock": asyncio.Lock()}
        for i in range(0, len(exists_products_sku), step):
            chunk = exists_products_sku[i: i + step]
            chunks.append(
                get_sku_info(
                    session, semaphore, token, chunk, skus_full_info, message, counter, len(exists_products_sku)
                )
            )
        await asyncio.gather(*chunks)

    await message.answer(f"Обработка штрих-кодов завершена!")

    for sku in skus_full_info:
        shk_ids = sku_shk_dict[str(sku.pop("sku_id"))]
        for shk_id in shk_ids:
            shk_dict[shk_id] = sku

    result = [item for item in shk_dict.values() if item]
    df = pandas.DataFrame(result)
    df.rename(
        columns={
            "name": "Названия",
            "category": "Категория",
            "subcategory": "Подкатегория",
            "nm_id": "Артикул",
        },
        inplace=True,
    )

    return df, token
