import jwt

class JWTDecoder:
    def __init__(self, token: str):
        self.token = token

    def get_token_headers(self):
        """Helper function to get the headers of a JWT token.
            If the token is invalid, it will raise an exception.

        Returns:
            if valid token: {'alg': str, 'typ': str}
            else: {"error": "Invalid token"}
        """
        try:
            return jwt.get_unverified_header(self.token[7:]) # Remove "Bearer " from the token.
        except jwt.exceptions.DecodeError:
            return {"error": "Invalid token"}
