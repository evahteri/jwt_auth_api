import uvicorn
from typing import Annotated
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from services.jwt_decoder import JWTDecoder
from services.header_validator import HeaderValidator

app = FastAPI()

class JWTValidity(BaseModel):
    valid: bool 

@app.get("/auth", response_model=JWTValidity)
async def index(Authorization: Annotated[str | None, Header()]):
    jwt_validity = True
    token_headers = JWTDecoder(token=Authorization).get_token_headers()
    if "error" in token_headers:
        raise HTTPException(status_code=422, detail=token_headers["error"])
    HeaderValidator(headers=token_headers).validate_headers()
    return JWTValidity(valid=jwt_validity)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)