import pytest
from helpers.api_client import StellarBurgersApi
from helpers.data_generator import generate_random_email, generate_random_password


@pytest.fixture
def api():
    return StellarBurgersApi()


@pytest.fixture
def user_data():
    return {
        "email": generate_random_email(),
        "password": generate_random_password(),
        "name": "Test User"
    }


@pytest.fixture
def registered_user(api, user_data):
    response = api.register_user(user_data)
    response.raise_for_status()
    data = response.json()

    yield {
        **user_data,
        "accessToken": data["accessToken"],
        "refreshToken": data["refreshToken"]
    }

    api.delete_user(data["accessToken"])


@pytest.fixture
def ingredients(api):
    response = api.get_ingredients()
    response.raise_for_status()
    return [item["_id"] for item in response.json()["data"]]
