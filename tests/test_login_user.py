import allure
import pytest


@allure.feature("Логин пользователя")
class TestLoginUser:

    @allure.title("Логин под существующим пользователем")
    def test_login_existing_user(self, api, registered_user):
        payload = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = api.login_user(payload)
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert "accessToken" in body
        assert "refreshToken" in body
        assert body["user"]["email"] == registered_user["email"]

    @allure.title("Логин с неверным логином и паролем")
    @pytest.mark.parametrize("wrong_field", ["email", "password", "both"])
    def test_login_with_invalid_credentials(self, api, registered_user, wrong_field):
        payload = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }

        if wrong_field in ("email", "both"):
            payload["email"] = "wrong_" + payload["email"]
        if wrong_field in ("password", "both"):
            payload["password"] = "wrong_password_123"

        response = api.login_user(payload)
        body = response.json()

        assert response.status_code == 401
        assert body["success"] is False
        assert body["message"] == "email or password are incorrect"