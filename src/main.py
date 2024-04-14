import uvicorn
from typing import Annotated
from fastapi import FastAPI, Header
from pydantic import BaseModel
from services.jwt_decoder import JWTDecoder
from services.header_validator import HeaderValidator
from services.signature_validator import SignatureValidator
from services.custom_expiration_validator import ExpirationValidator

app = FastAPI()

class JWTValidity(BaseModel):
    valid: bool

@app.get("/auth", response_model=JWTValidity)
async def index(Authorization: Annotated[str | None, Header()]) -> JWTValidity:
    token_headers = JWTDecoder(token=Authorization).get_token_headers() # Extract token headers
    HeaderValidator(headers=token_headers).validate_headers() # Validate token headers
    token_payload = await SignatureValidator(token=Authorization, x5u=token_headers["x5u"]).validate_signature() # Validate token signature
    ExpirationValidator(
        token_payload=token_payload).validate_expiration() # Validate custom token expiration (max time to live)
    return JWTValidity(valid=True) # Return a valid response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
