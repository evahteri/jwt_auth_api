import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_index_empty_get():
    """An empty GET request should return a 422 (unprocessable entity) status code with an explanation.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/auth")
        assert response.status_code == 422
        assert response.json()["detail"][0]["type"] == "missing"
        assert response.json()["detail"][0]["loc"] == ["header", "Authorization"]
        assert response.json()["detail"][0]["msg"] == "Field required"

@pytest.mark.asyncio
async def test_index_get_RS512():
    """A GET request with wrong signature algorithm should return a 422 (unprocessable entity) status code with an explanation.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/auth", headers={"Authorization": "Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.pazba9Pj009HgANP4pTCQAHpXNU7pVbjIGff_plktSzsa9rXTGzFngaawzXGEO6Q0Hx5dtGi-dMDlIadV81o3Q"})
        assert response.status_code == 422
        assert response.json()["detail"].startswith("Invalid algorithm")

@pytest.mark.asyncio
async def test_index_post():
    """A POST request should return a 405 status code.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/auth")
        assert response.status_code == 405
        assert response.json() == {"detail": "Method Not Allowed"}

@pytest.mark.asyncio
async def test_index_put():
    """A PUT request should return a 405 status code.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.put("/auth")
        assert response.status_code == 405
        assert response.json() == {"detail": "Method Not Allowed"}

@pytest.mark.asyncio
async def test_index_delete():
    """A DELETE request should return a 405 status code.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.delete("/auth")
        assert response.status_code == 405
        assert response.json() == {"detail": "Method Not Allowed"}