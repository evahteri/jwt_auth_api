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
        try:
            print(pyjwt.get_unverified_header(self.token[7:]))
            return pyjwt.get_unverified_header(self.token[7:]) # Remove "Bearer " from the token.
        except pyjwt.exceptions.DecodeError as e:
            return {"error": str(e)}

