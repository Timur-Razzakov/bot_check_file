import hashlib
import hmac

class Signature:
    def __init__(self, request, secret_key):
        self.request = request
        self.secret_key = secret_key

    def generate_signature(self, request_body: dict) -> str:
        sorted_keys = sorted(request_body.keys())
        concatenated_values = ".".join(str(request_body[key]) for key in sorted_keys)
        concatenated_values += self.secret_key
        signature = hmac.new(
            key=self.secret_key.encode(),
            msg=concatenated_values.encode(),
            digestmod=hashlib.sha256,
        ).hexdigest()
        return signature

    def add_signature_to_headers(self, request_body: dict, headers: dict) -> dict:
        signature = self.generate_signature(request_body)
        headers['X-Request-Sign'] = signature
        return headers

