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
async def test_auth_missing_x5u_header():
    """A GET request with a missing x5u header should return a 422 (unprocessable entity) status code with an explanation.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/auth", headers={"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.NHVaYe26MbtOYhSKkoKYdFVomg4i8ZJd8_-RU8VNbftc4TSMb4bXP3l3YlNWACwyXPGffz5aXHc6lty1Y2t4SWRqGteragsVdZufDn5BlnJl9pdR_kdVFUsra2rWKEofkZeIC4yWytE58sMIihvo9H1ScmmVwBcQP6XETqYd0aSHp1gOa9RdUPDvoXQ5oqygTqVtxaDr6wUFKrKItgBMzWIdNZ6y7O9E0DhEPTbE9rfBo6KTFsHAZnMg4k68CDp2woYIaXbmYTWcvbzIuHO7_37GT79XdIwkm95QJ7hYC9RiwrV7mesbY4PAahERJawntho0my942XheVLmGwLMBkQ"})
        assert response.status_code == 422
        assert response.json()["detail"].startswith("Invalid token headers")


@pytest.mark.asyncio
async def test_auth_missing_typ_header():
    """A GET request with a missing typ header should return a 422 (unprocessable entity) status code with an explanation.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/auth", headers={"Authorization": "Bearer eyJ4NXUiOiJodHRwczovL2V4YW1wbGUuY29tL2NlcnQucGVtIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.PG0Ys4-PYWVa84PGr9WXqWUoHuHoUrwhC8blef8cnsnzmev7c2KG10SAvnM-kTuO7V29t6eNdpruCDBXImQMT535Eh8LNXXb2XqS7xBbQXKaa7rBulcLDh-gv-iXwYQ6mZrWXb6iXkn4n7NbONN627kH5i-mbnK7vDXm6V7gQiRnhkgPAqvfcdCcZQsCoR0QJeiHMLDgvxEJm2L6YHiJDUehJT_xTZxq3pgjdNSxwEUoEB2hhdMRoG-Jt6qrBlSTg9xrRHomHfp1cgwMFnzGTYW8tXiCNsN3ycFTyjLkKMqzcyqB_xIkWrGbo0CZI3qNCvhjDmzDBqA7AZfojGu7uA"})
        assert response.status_code == 422
        assert response.json()["detail"].startswith("Invalid token headers")


@pytest.mark.asyncio
async def test_auth_get_HS512():
    """A GET request with wrong signature algorithm should return a 422 (unprocessable entity) status code with an explanation.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/auth", headers={"Authorization": "Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCIsIng1dSI6Imh0dHBzOi8vZXhhbXBsZS5jb20vY2VydC5wZW0ifQ.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.9kns8MAo9FAf5ggLQkR7LxVBU6nSmGCl8vu5EDUYwvaOjwBSwYAD6c1c3RE1Dn39EolOitEQKMzV3SNB8llCrw"})
        assert response.status_code == 422
        assert response.json()["detail"].startswith("Invalid algorithm")


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
