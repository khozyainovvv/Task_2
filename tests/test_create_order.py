import allure


@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_authorized_with_ingredients(self, api, registered_user, ingredients):
        payload = {"ingredients": ingredients[:2]}
        response = api.create_order(payload, token=registered_user["accessToken"])
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert "order" in body
        assert "number" in body["order"]

    @allure.title("Создание заказа без авторизации (API разрешает, расхождение с докой)")
    def test_create_order_unauthorized(self, api, ingredients):
        payload = {"ingredients": ingredients[:2]}
        response = api.create_order(payload)
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert "order" in body

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, api, registered_user):
        response = api.create_order(
            {"ingredients": []},
            token=registered_user["accessToken"]
        )
        body = response.json()

        assert response.status_code == 400
        assert body["success"] is False
        assert body["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с неверным хешем ингредиента")
    def test_create_order_with_invalid_ingredient_hash(self, api, registered_user):
        payload = {"ingredients": ["invalid_hash_123"]}
        response = api.create_order(payload, token=registered_user["accessToken"])

        assert response.status_code == 500