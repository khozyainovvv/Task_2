import allure
import pytest


@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, api, user_data):
        response = api.register_user(user_data)
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert "accessToken" in body
        assert "refreshToken" in body
        assert body["user"]["email"] == user_data["email"]
        assert body["user"]["name"] == user_data["name"]

        api.delete_user(body["accessToken"])

    @allure.title("Создание уже зарегистрированного пользователя")
    def test_create_existing_user(self, api, registered_user):
        payload = {
            "email": registered_user["email"],
            "password": registered_user["password"],
            "name": registered_user["name"]
        }
        response = api.register_user(payload)
        body = response.json()

        assert response.status_code == 403
        assert body["success"] is False
        assert body["message"] == "User already exists"

    @allure.title("Создание пользователя без обязательного поля: {missing_field}")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_without_required_field(self, api, user_data, missing_field):
        payload = {k: v for k, v in user_data.items() if k != missing_field}
        response = api.register_user(payload)
        body = response.json()

        assert response.status_code == 403
        assert body["success"] is False
        assert body["message"] == "Email, password and name are required fields"