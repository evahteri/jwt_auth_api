import pytest
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.mark.asyncio
async def test_auth_empty_get():
    """An empty GET request should return a 422 (unprocessable entity) status code with an explanation.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/auth")
        assert response.status_code == 422
        assert response.json()["detail"][0]["type"] == "missing"
        assert response.json()["detail"][0]["loc"] == [
            "header", "Authorization"]
        assert response.json()["detail"][0]["msg"] == "Field required"


@pytest.mark.asyncio
async def test_auth_post():
    """A POST request should return a 405 status code.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/auth")
        assert response.status_code == 405
        assert response.json() == {"detail": "Method Not Allowed"}


@pytest.mark.asyncio
async def test_auth_put():
    """A PUT request should return a 405 status code.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.put("/auth")
        assert response.status_code == 405
        assert response.json() == {"detail": "Method Not Allowed"}


@pytest.mark.asyncio
async def test_auth_delete():
    """A DELETE request should return a 405 status code.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.delete("/auth")
        assert response.status_code == 405
        assert response.json() == {"detail": "Method Not Allowed"}
