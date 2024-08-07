import logging

import aiohttp


async def get_products_by_shk_id(session: aiohttp.ClientSession, token: str, shk_id: str) -> str | None:
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru,en;q=0.9,la;q=0.8,tr;q=0.7",
        "authorization": f"Bearer {token}",
        "priority": "u=1, i",
        "referer": f"https://wms.wbwh.tech/shk-v2/status?shk={shk_id}",
        "sec-ch-ua": '"Chromium";v="124", "YaBrowser";v="24.6", "Not-A.Brand";v="99", "Yowser";v="2.5"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, как Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36",
    }

    params = {
        "goods_sticker": shk_id,
    }
    url = "https://wms.wbwh.tech/srv/wms_front_cut_shk_repo_cluster_api_proxy/api/get_by_goods_sticker"

    try:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data["data"]["sku_id"]
            logging.error(f"Error {response.status}: {response.reason} for shk_id: {shk_id}")
            return None
    except aiohttp.ClientConnectorError as e:
        logging.error(f"Connection error for shk_id: {shk_id}: {str(e)}")
        return None


async def get_products_full_info(session: aiohttp.ClientSession, token: str, sku_ids: list[int]) -> list[dict]:
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru",
        "authorization": f"Bearer {token}",
        "content-type": "application/json",
        "origin": "https://wms.wbwh.tech",
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
    json_data = {
        "chrt_ids": sku_ids,
    }
    url = "https://wms.wbwh.tech/srv/wms_front_proxy_cut_barcode_chrt_repository_api/api/chrt/info"
    try:
        async with session.post(url, headers=headers, json=json_data) as response:
            if response.status == 200:
                data = await response.json()
                result = []
                for item in data["data"]:
                    result.append(
                        {
                            "sku_id": item.get("chrt_id", ""),
                            "name": item.get("imt_name", ""),
                            "category": item.get("subject_name_parent", ""),
                            "subcategory": item.get("subject_name", ""),
                            "nm_id": item.get("nm_id", 0),
                        }
                    )
                return result
            else:
                logging.error("AAAAAAAAAAAAAAAAAAA", await response.text())
            return []
    except aiohttp.ClientConnectorError as e:
        logging.error(f"Connection error for sku_ids: {sku_ids}: {str(e)}")
    return []
