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
    jwt_validity = True
    token_headers = JWTDecoder(token=Authorization).get_token_headers()
    jwt_validity = HeaderValidator(headers=token_headers).validate_headers()
    token_payload = await SignatureValidator(token=Authorization, x5u=token_headers["x5u"]).validate_signature()
    jwt_validity = ExpirationValidator(
        token_payload=token_payload).validate_expiration()
    return JWTValidity(valid=jwt_validity)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
