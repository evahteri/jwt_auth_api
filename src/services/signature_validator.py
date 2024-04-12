import httpx
import jwt as pyjwt
from fastapi import HTTPException


class SignatureValidator:
    def __init__(self, token: str, x5u: str) -> dict:
        self.token = token
        self.x5u = x5u

    async def validate_signature(self):
        """Helper function to validate the signature of a JWT token.
            If the token is invalid, it will raise an exception.

        Returns:
            if valid token: True
            else: {"error": "Invalid signature"}
        """

        try:
            response = httpx.get(self.x5u)
            if response.status_code != 200:
                raise HTTPException(status_code=422, detail={"message": "Invalid x5u. The certificate could not be retrieved.",
                                                             "detail": "The url provided in x5u responded with a " + str(response.status_code) + " status code."})
            key = response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=422, detail={"message": "Invalid x5u. The certificate could not be retrieved.",
                                                         "detail": e})
        except TypeError:
            raise HTTPException(status_code=422, detail={"message": "Invalid x5u. The certificate could not be retrieved.",
                                                         "detail": e})
        try:
            return pyjwt.decode(self.token[7:], key=key, algorithms=["RS256"])
        except pyjwt.ImmatureSignatureError:
            raise HTTPException(status_code=422, detail={"message": "Invalid iat. The certificate could not be validated.",
                                                         "detail": "The token is not yet valid (iat)"})
        except pyjwt.ExpiredSignatureError:
            raise HTTPException(status_code=422, detail={"message": "Invalid iat. The certificate could not be validated.",
                                                         "detail": "Signature has expired"})
