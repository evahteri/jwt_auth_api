import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class JWTValidity(BaseModel):
    valid: bool 

@app.get("/", response_model=JWTValidity)
async def index():
    # JWT validation logic go here
    jwt_validity = False
    if not jwt_validity:
        raise HTTPException(status_code=400, detail="Missing headers or invalid JWT.")
    return JWTValidity(valid=jwt_validity)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)