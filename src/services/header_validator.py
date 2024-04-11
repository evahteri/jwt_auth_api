from fastapi import HTTPException


class HeaderValidator:
    def __init__(self, headers: dict):
        self.headers = headers

    def validate_headers(self) -> bool:
        required_headers = ["x5u", "alg", "typ"]
        missing_headers = [
            header for header in required_headers if header not in self.headers]
        if missing_headers:
            raise HTTPException(
                status_code=422, detail=f"Invalid token headers. {', '.join(missing_headers)} header(s) is missing.")
        if self.headers["alg"] != "RS256":
            raise HTTPException(
                status_code=422, detail=f"Invalid algorithm. Alg header is {self.headers['alg']}. The API is configured to use RS256.")
        if self.headers["typ"] != "JWT":
            raise HTTPException(
                status_code=422, detail=f"Invalid token type. Typ header is {self.headers['typ']}. The API is configured to use JWT.")
        return True
