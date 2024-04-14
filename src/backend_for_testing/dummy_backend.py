import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/pubkey.pem")
async def get_cert():
    """This endpoint is for testing purposes.
    Check README for instructions on how to create a private/public key pair and a corresbonding JWT.
    The endpoint returns the contents of the .pem file.
    """
    public_key = open('test_public_key.pem', 'r').read()
    return public_key.strip()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)