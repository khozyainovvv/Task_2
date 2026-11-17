import requests
from helpers.config import BASE_URL


class StellarBurgersApi:

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
    