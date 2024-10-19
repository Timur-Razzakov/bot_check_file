import httpx

from data.config import SECRET_KEY
from services.signature import Signature


class PassportChecker():
    @staticmethod
    def get_details(params, url, headers=None):
        try:
            with httpx.Client(timeout=80.0) as client:  # Указываем тайм-аут 30 секунд
                response = client.post(
                    url,
                    headers=headers,
                    json=params,
                )
                response.raise_for_status()  # Поднимет исключение, если статус код не 200

                # Если ответ успешный, возвращаем JSON-ответ
                return response.json()
        except httpx.ReadTimeout:
            # Обработка тайм-аута
            return {"error": "Request timed out", "response": None}
        except httpx.RequestError as exc:
            # Обработка других ошибок запроса
            return {"error": f"An error occurred while requesting {exc.request.url!r}.", "response": None}

    def passport_pinfl_is_correct(self, pinfl: str,
                                  passport_serial_number: str,
                                  ):
        url = "http://185.196.213.130:8081/api/v1/passport/is_correct"
        headers = {
            "Content-Type": "application/json",
        }
        params = {
            "pinfl": pinfl,
            "passport_serial_number": passport_serial_number,
        }
        signed_headers = Signature(
            request=self.request, secret_key=SECRET_KEY
        ).add_signature_to_headers(params, headers)
        individual_details = self.get_details(params=params, url=url, headers=signed_headers)
        if 'code' in individual_details:
            code = individual_details['code']
            print(f"Received code: {code}")
            return code
        else:
            # Обрабатываем случай отсутствия кода в ответе
            error_message = individual_details.get('error', 'Unknown error')
            print(f"Error retrieving code: {error_message}")
            return None
