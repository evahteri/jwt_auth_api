import httpx
import jwt as pyjwt
from fastapi import HTTPException


class SignatureValidator:
    def __init__(self, token: str, x5u: str):
        self.token = token
        self.x5u = x5u

    async def validate_signature(self) -> dict:
        """Helper function to validate the signature of a JWT token.
            If the token is invalid, it will raise an exception.
        """
        try:
            # Using async for improved performance.
            async with httpx.AsyncClient() as client:
                response = await client.get(self.x5u)
                # Raise an exception for 4xx and 5xx status codes.
                response.raise_for_status()

                key = response.json()
            return pyjwt.decode(self.token[7:], key=key, algorithms=["RS256"])

        except httpx.HTTPStatusError:
            raise HTTPException(
                status_code=422, detail=f"Invalid x5u. The certificate could not be retrieved. The url provided in x5u responded with a {response.status_code} status code.")
        except httpx.HTTPError as e:
            # This error is raised when the request to x5u URL fails.
            raise HTTPException(
                status_code=422, detail=f"Invalid x5u. The certificate could not be retrieved. Error: {e}")
        except pyjwt.ImmatureSignatureError:
            # ImmatureSignatureError is raised when the token is not yet valid.
            raise HTTPException(
                status_code=422, detail="Invalid iat. The certificate could not be validated. The token is not yet valid (iat)")
        except pyjwt.ExpiredSignatureError:
            # ExpiredSignatureError is raised when the token has expired.
            raise HTTPException(
                status_code=422, detail="Invalid iat. The certificate could not be validated. Signature has expired")
