from fastapi import HTTPException
import jwt as pyjwt


class JWTDecoder:
    def __init__(self, token: str):
        self.token = token

    def get_token_headers(self) -> dict:
        """Helper function to get the headers of a JWT token.
            If the token is invalid, it will raise an exception.

        Returns:
            if valid token: dictionary including the headers.
            else: {"error": "Invalid token"}
        """
        if " " in self.token[7:]:
            raise HTTPException(status_code=422, detail="Invalid token. The token should not contain any spaces.")
        try:
            return pyjwt.get_unverified_header(self.token[7:])
        except pyjwt.exceptions.DecodeError as e:
            raise HTTPException(status_code=422, detail=e)
