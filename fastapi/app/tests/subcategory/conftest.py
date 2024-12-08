import pytest
import pytest_asyncio
from uuid import uuid4
from httpx import AsyncClient
from starlette.status import HTTP_200_OK, HTTP_201_CREATED


@pytest_asyncio.fixture(scope="session")
def category_data():
    """Fixture to provide category data."""
    return {"name": str(uuid4())}


@pytest_asyncio.fixture(scope="session")
def sub_category_data():
    """Fixture to provide category data."""
    return {"name": str(uuid4())}


@pytest.fixture(scope="module")
async def category(client: AsyncClient, category_data: dict):
    # Create category
    response = await client.post("/api/v1/category/create", json=category_data)
    response_json = response.json()
    assert response.status_code == HTTP_201_CREATED
    assert response_json["name"] == category_data["name"]

    category_id = response_json["id"]
    yield category_id  # Return the category ID to the test

    # Cleanup: Delete category
    response = await client.delete(f"/api/v1/category/{category_id}")
    response_json = response.json()
    assert response.status_code == HTTP_200_OK
    assert response_json["id"] == category_id