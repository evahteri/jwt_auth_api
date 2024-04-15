from fastapi import HTTPException
import jwt as pyjwt


class JWTDecoder:
    def __init__(self, token: str):
        self.token = token

    def get_token_headers(self) -> dict:
        """Helper function to get the headers of a JWT token.
            If the token is invalid, it will raise an exception.

        Returns:
            if the token is valid: dictionary including the headers.
        """
        if len(self.token) < 512 or self.token[:7] != "Bearer ":
            raise HTTPException(
                status_code=400, detail="Invalid token. The token should start with 'Bearer ', And should be at least 512 characters long.")
        if " " in self.token[7:]:
            raise HTTPException(
                status_code=400, detail="Invalid token. The token should not contain any spaces.")
        try:
            # Here the validation is not yet done, only fetching the headers.
            return pyjwt.get_unverified_header(self.token[7:])
        except pyjwt.exceptions.DecodeError as e:
            # This error is raised when the token is invalid.
            raise HTTPException(status_code=422, detail=e)
