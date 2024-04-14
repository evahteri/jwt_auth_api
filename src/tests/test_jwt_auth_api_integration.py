import pytest
from datetime import datetime
from httpx import AsyncClient, ASGITransport
from main import app
from backend_for_testing.jwt_generator import JWTGenerator
# These integration tests a use dummy backend.
# Run dummy_backend.py in the background when running these tests

@pytest.mark.asyncio
async def test_auth_valid_token_returns_200():
    """A GET request with a valid token should return 200 with { "valid": true } json.
    """
    iat = int(datetime.now().timestamp())

    valid_jwt_token = JWTGenerator().generate_jwt_token(iat=iat, exp=iat + 5000, x5u="http://localhost:3000/pubkey.pem" ,typ="JWT", alg= "RS256")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:

        response = await ac.get("/auth", headers={"Authorization": f"Bearer {valid_jwt_token}"})
        assert response.status_code == 200
        assert response.json() == {"valid": True}

@pytest.mark.asyncio
async def test_auth_invalid_token_iat_not_yet_active():
    """A GET request with a token that is not yet active should return 422 with an explanation.
    """
    iat = int(datetime.now().timestamp())

    valid_jwt_token = JWTGenerator().generate_jwt_token(iat=iat + 5000, exp=iat + 10000, x5u="http://localhost:3000/pubkey.pem" ,typ="JWT", alg= "RS256")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:

        response = await ac.get("/auth", headers={"Authorization": f"Bearer {valid_jwt_token}"})
        assert response.status_code == 422
        assert response.json()["detail"]["detail"] == "The token is not yet valid (iat)"