import random
import string

import pytest
import requests

BASE_URL = "https://stellarburgers.education-services.ru/api"


def generate_random_email() -> str:
    return f"test_{random.randint(100000, 999999)}@yandex.ru"


def generate_random_password() -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


class ApiClient:

    @staticmethod
    def register_user(payload: dict) -> requests.Response:
        return requests.post(f"{BASE_URL}/auth/register", json=payload)

    @staticmethod
    def login_user(payload: dict) -> requests.Response:
        return requests.post(f"{BASE_URL}/auth/login", json=payload)

    @staticmethod
    def update_user(payload: dict, token: str = None) -> requests.Response:
        headers = {"Authorization": token} if token else {}
        return requests.patch(f"{BASE_URL}/auth/user", json=payload, headers=headers)

    @staticmethod
    def delete_user(token: str) -> requests.Response:
        return requests.delete(f"{BASE_URL}/auth/user", headers={"Authorization": token})

    @staticmethod
    def create_order(payload: dict, token: str = None) -> requests.Response:
        headers = {"Authorization": token} if token else {}
        return requests.post(f"{BASE_URL}/orders", json=payload, headers=headers)

    @staticmethod
    def get_user_orders(token: str = None) -> requests.Response:
        headers = {"Authorization": token} if token else {}
        return requests.get(f"{BASE_URL}/orders", headers=headers)

    @staticmethod
    def get_ingredients() -> requests.Response:
        return requests.get(f"{BASE_URL}/ingredients")


@pytest.fixture
def api():
    return ApiClient()


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

@pytest.fixture
def random_email():
    return generate_random_email()


@pytest.fixture
def random_password():
    return generate_random_password()