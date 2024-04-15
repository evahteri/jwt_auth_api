import uvicorn
from fastapi import FastAPI
import os

app = FastAPI()


@app.get("/pubkey.pem")
async def get_cert():
    """This endpoint is for testing purposes.
    Check README for instructions on how to create a private/public key pair and a corresbonding JWT.
    The endpoint returns the contents of the .pem file.
    """
    file_path_public_key = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "test_public_key.pem")
    with open(file_path_public_key, "r") as f:
        public_key = f.read()
    return public_key.strip()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
