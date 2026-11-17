import allure
import pytest
from helpers.constants import MSG_UNAUTHORIZED
from helpers.data_generator import generate_random_email, generate_random_password


@allure.feature("Изменение данных пользователя")
class TestUpdateUser:

    @allure.title("Изменение email с авторизацией")
    def test_update_email_authorized(self, api, registered_user):
        new_email = generate_random_email()
        response = api.update_user(
            {"email": new_email},
            token=registered_user["accessToken"]
        )
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert body["user"]["email"] == new_email

    @allure.title("Изменение пароля с авторизацией")
    def test_update_password_authorized(self, api, registered_user):
        new_password = generate_random_password()
        response = api.update_user(
            {"password": new_password},
            token=registered_user["accessToken"]
        )
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True

        login = api.login_user({
            "email": registered_user["email"],
            "password": new_password
        })
        assert login.status_code == 200

    @allure.title("Изменение имени с авторизацией")
    def test_update_name_authorized(self, api, registered_user):
        response = api.update_user(
            {"name": "New Name"},
            token=registered_user["accessToken"]
        )
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert body["user"]["name"] == "New Name"

    @allure.title("Изменение данных без авторизации")
    @pytest.mark.parametrize("field, value", [
        ("email", "new_email@yandex.ru"),
        ("password", "new_password"),
        ("name", "New Name"),
    ])
    def test_update_user_unauthorized(self, api, field, value):
        response = api.update_user({field: value})
        body = response.json()

        assert response.status_code == 401
        assert body["success"] is False
        assert body["message"] == MSG_UNAUTHORIZED
        