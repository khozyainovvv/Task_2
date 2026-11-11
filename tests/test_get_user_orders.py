import allure


@allure.feature("Получение заказов пользователя")
class TestGetUserOrders:

    @allure.title("Получение заказов авторизованным пользователем")
    def test_get_orders_authorized(self, api, registered_user, ingredients):
        api.create_order(
            {"ingredients": ingredients[:1]},
            token=registered_user["accessToken"]
        )

        response = api.get_user_orders(token=registered_user["accessToken"])
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert "orders" in body
        assert isinstance(body["orders"], list)

    @allure.title("Получение заказов неавторизованным пользователем")
    def test_get_orders_unauthorized(self, api):
        response = api.get_user_orders()
        body = response.json()

        assert response.status_code == 401
        assert body["success"] is False
        assert body["message"] == "You should be authorised"