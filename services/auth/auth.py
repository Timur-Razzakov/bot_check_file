import json
import os

import aiohttp

TOKEN_FILE_PATH = "./tgbot/services/auth/token.json"


async def login(employee_id: int, password: str) -> tuple[str | None, str | None]:
    # Первый возвращаемый аргумент это токен если он есть,
    # а второй это ошибка если она есть
    url = "https://wms.wbwh.tech/srv/auth_employee_id/api/login/ep"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru,en;q=0.9,la;q=0.8,tr;q=0.7",
        "content-type": "application/json",
        "origin": "https://wms.wbwh.tech",
        "priority": "u=1, i",
        "referer": "https://wms.wbwh.tech/login",
        "sec-ch-ua": '"Chromium";v="124", "YaBrowser";v="24.6", "Not-A.Brand";v="99", "Yowser";v="2.5"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36",
    }

    json_data = {
        "employee_id": employee_id,
        "password": password,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=json_data) as response:
            print(await response.text(), response.status)
            if response.status == 200:
                data = await response.json()
                with open(TOKEN_FILE_PATH, "w", encoding="utf-8") as file:
                    json.dump(data["data"], file, ensure_ascii=False)
                return data["data"]["access_token"], None

            return None, f"{await response.text()} !!!!-!!!! {response.status}"


async def check_token(token: str | None) -> bool:
    if not token:
        return False

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru,en;q=0.9,la;q=0.8,tr;q=0.7",
        "authorization": f"Bearer {token}",
        "priority": "u=1, i",
        "referer": "https://wms.wbwh.tech/shk-v2/status",
        "sec-ch-ua": '"Chromium";v="124", "YaBrowser";v="24.6", "Not-A.Brand";v="99", "Yowser";v="2.5"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36",
    }

    async with aiohttp.ClientSession() as session:
        async with session.get("https://wms.wbwh.tech/srv/auth_token/api/login/check", headers=headers) as response:
            return response.status == 200


async def get_access_token(employee_id: int, password: str) -> tuple[str | None, str | None]:
    token_data = {}
    if os.path.exists(TOKEN_FILE_PATH):
        with open(TOKEN_FILE_PATH, "r", encoding="utf-8") as f:
            token_data = json.load(f)

    token = token_data.get("access_token", None)
    if not await check_token(token):
        return await login(employee_id=employee_id, password=password)

    return token, None
