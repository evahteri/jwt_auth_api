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

    jwt_token = JWTGenerator().generate_jwt_token(iat=iat + 5000, exp=iat + 10000, x5u="http://localhost:3000/pubkey.pem" ,typ="JWT", alg= "RS256")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:

        response = await ac.get("/auth", headers={"Authorization": f"Bearer {jwt_token}"})
        assert response.status_code == 422
        assert response.json()["detail"]["detail"] == "The token is not yet valid (iat)"

@pytest.mark.asyncio
async def test_auth_invalid_token_not_RS256():
    """A GET request with a token that is not signed with RS256 should return 422 with an explanation.
    """
    iat = int(datetime.now().timestamp())

    jwt_token = JWTGenerator().generate_jwt_token(iat=iat, exp=iat + 5000, x5u="http://localhost:3000/pubkey.pem" ,typ="JWT", alg= "RS512")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:

        response = await ac.get("/auth", headers={"Authorization": f"Bearer {jwt_token}"})
        assert response.status_code == 422
        assert response.json()["detail"] == "Invalid algorithm. Alg header is RS512. The API is configured to use RS256."

@pytest.mark.asyncio
async def test_auth_invalid_token_typ_not_JWT():
    """A GET request with a token that has a typ header that is not JWT should return 422 with an explanation.
    """
    iat = int(datetime.now().timestamp())

    jwt_token = JWTGenerator().generate_jwt_token(iat=iat, exp=iat + 5000, x5u="http://localhost:3000/pubkey.pem" ,typ="AT", alg= "RS256")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:

        response = await ac.get("/auth", headers={"Authorization": f"Bearer {jwt_token}"})
        assert response.status_code == 422
        assert response.json()["detail"] == "Invalid token type. Typ header is AT. The API is configured to use JWT."

@pytest.mark.asyncio
async def test_auth_invalid_token_missing_x5u_header():
    """A GET request with a token that is missing the x5u header should return 422 with an explanation.
    """
    iat = int(datetime.now().timestamp())

    jwt_token = JWTGenerator().generate_jwt_token(iat=iat, exp=iat + 5000, typ="AT", alg= "RS256")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:

        response = await ac.get("/auth", headers={"Authorization": f"Bearer {jwt_token}"})
        assert response.status_code == 422
        assert response.json()["detail"] == "Invalid token headers. x5u header(s) is missing."

@pytest.mark.asyncio
async def test_auth_invalid_token_missing_typ_header():
    """A GET request with a token that is missing the typ header should return 422 with an explanation.
    """
    iat = int(datetime.now().timestamp())

    jwt_token = JWTGenerator().generate_jwt_token(iat=iat, exp=iat + 5000, x5u="http://localhost:3000/pubkey.pem", alg= "RS256")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:

        response = await ac.get("/auth", headers={"Authorization": f"Bearer {jwt_token}"})
        assert response.status_code == 422
        assert response.json()["detail"] == "Invalid token headers. typ header(s) is missing."

@pytest.mark.asyncio
async def test_auth_invalid_token_invalid_authorization_header_format():
    """A GET request with a token that has an invalid Authorization header format should return 422 with an explanation.
    """
    iat = int(datetime.now().timestamp())

    jwt_token = JWTGenerator().generate_jwt_token(iat=iat, exp=iat + 5000, x5u="http://localhost:3000/pubkey.pem" ,typ="JWT", alg= "RS256")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:

        response = await ac.get("/auth", headers={"Authorization": f"Bearer  {jwt_token}"})
        assert response.status_code == 422
        assert response.json()["detail"] == "Invalid token. The token should not contain any spaces."

@pytest.mark.asyncio
async def test_auth_invalid_token_invalid_authorization_header_format_typo():
    """A GET request with a token that has an invalid Authorization header format (Beaer != Bearer) should return 422 with an explanation.
    """
    iat = int(datetime.now().timestamp())

    jwt_token = JWTGenerator().generate_jwt_token(iat=iat, exp=iat + 5000, x5u="http://localhost:3000/pubkey.pem" ,typ="JWT", alg= "RS256")

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:

        response = await ac.get("/auth", headers={"Authorization": f"Beaer  {jwt_token}"})
        assert response.status_code == 422
        assert response.json()["detail"] == "Invalid token. The token should start with 'Bearer ', And should be at least 512 characters long."