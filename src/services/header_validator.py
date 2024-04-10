import configuration
from fastapi import HTTPException

class HeaderValidator:
    def __init__(self, headers: dict):
        self.headers = headers

    def validate_headers(self):
        if self.headers["alg"] != configuration.ALGORITHM:
            raise HTTPException(status_code=422, detail=f"Invalid algorithm. Alg header is {self.headers['alg']}. The API is configured to use {configuration.ALGORITHM}.")
        if self.headers["typ"] != "JWT":
            raise HTTPException(status_code=422, detail=f"Invalid token type. Typ header is {self.headers['typ']}. The API is configured to use JWT.")
        return True