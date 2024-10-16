import httpx


class PassportChecker():
    @staticmethod
    def get_details(params, url, headers=None):
        with httpx.Client() as client:
            response = client.post(
                url,
                headers=headers,
                json=params,
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": f"Failed to get details. Status code: {response.status_code}",
                    "response": response.text
                }

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
        individual_details = self.get_details(params=params, url=url, headers=headers)
        if 'code' in individual_details:
            code = individual_details['code']
            print(f"Received code: {code}")
            return code
        else:
            # Обрабатываем случай отсутствия кода в ответе
            error_message = individual_details.get('error', 'Unknown error')
            print(f"Error retrieving code: {error_message}")
            return None
