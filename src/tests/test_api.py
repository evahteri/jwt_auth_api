import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_index_empty_get():
    """An empty GET request should return a 400 status code.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
        assert response.status_code == 400

@pytest.mark.asyncio
async def test_index_post():
    """A POST request should return a 405 status code.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/")
        assert response.status_code == 405
        assert response.json() == {"detail": "Method Not Allowed"}

@pytest.mark.asyncio
async def test_index_put():
    """A PUT request should return a 405 status code.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.put("/")
        assert response.status_code == 405
        assert response.json() == {"detail": "Method Not Allowed"}

@pytest.mark.asyncio
async def test_index_delete():
    """A DELETE request should return a 405 status code.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.delete("/")
        assert response.status_code == 405
        assert response.json() == {"detail": "Method Not Allowed"}