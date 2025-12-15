import allure
from PythonProject5.src.item_models.data_error_model import Error422, Error401, Error404
from PythonProject5.src.utils_item.validator_error_items import validate_error422, validate_error401, validate_error404


class TestInvalid:

    @allure.title("Тест на создание item с title более 255 символов")
    def test_create_too_long_title(self, invalid_create):
        item_obj = invalid_create.create_too_long_title()
        assert item_obj.status_code == 422, "Получен неожидаемый статус-код "
        item_json = item_obj.json()
        data = item_json["detail"][0]["type"]
        assert data == "string_too_long", "Получен неожидаемый текст"
        validate_error422(item_obj, model=Error422,
                      expected_data= item_json)
        assert len(item_json) > 0, "Ответ не должен быть пустым"

    @allure.title("Тест на создание item с пустым title")
    def test_create_non_title(self, invalid_create):
        item_obj = invalid_create.create_non_title()
        assert item_obj.status_code == 422, "Получен неожидаемый статус-код "
        item_json = item_obj.json()
        data = item_json["detail"][0]["type"]
        assert data == "string_too_short", "Получен неожидаемый текст"
        validate_error422(item_obj, model=Error422,
                      expected_data= item_json)
        assert len(item_json) > 0, "Ответ не должен быть пустым"

    @allure.title("Тест на создание item с пустым токеном")
    def test_create_empty_token(self, invalid_create):
        item_obj = invalid_create.create_empty_token()
        assert item_obj.status_code == 401, "Получен неожидаемый статус-код "
        item_json = item_obj.json()
        data = item_json["detail"]
        assert data == "Not authenticated", "Получен неожидаемый текст"
        validate_error401(item_obj, model=Error401,
                          expected_data=item_json)

    @allure.title("Тест на создание item, а затем попытка его получения с пустым токеном")
    def test_create_and_get_empty_token(self, invalid_item, cleanup_items):
        item_create,item_obj = invalid_item.create_and_get_empty_token()
        json_item_obj = item_create.json()
        item_id = json_item_obj.get("id")
        cleanup_items.append(item_id)
        assert item_create.status_code == 200, "Получен неожидаемый статус-код "
        assert len(json_item_obj) > 0, "JSON не должен быть пустым"
        assert item_obj.status_code == 401, "Получен неожидаемый статус-код "
        item_json = item_obj.json()
        data = item_json["detail"]
        assert data == "Not authenticated", "Получен неожидаемый текст"
        validate_error401(item_obj, model=Error401,
                          expected_data=item_json)

    @allure.title("Тест на создание item, а затем попытка обновления с пустым title")
    def test_create_and_update_empty_token(self, invalid_item, cleanup_items):
        item_create,item_obj = invalid_item.create_and_update_empty_token()
        json_item_obj = item_create.json()
        item_id = json_item_obj.get("id")
        cleanup_items.append(item_id)
        assert item_create.status_code == 200, "Получен неожидаемый статус-код "
        assert len(json_item_obj) > 0, "JSON не должен быть пустым"
        assert item_obj.status_code == 401, "Получен неожидаемый статус-код "
        item_json = item_obj.json()
        data = item_json["detail"]
        assert data == "Not authenticated", "Получен неожидаемый текст"
        validate_error401(item_obj, model=Error401,
                          expected_data=item_json)

    @allure.title("Тест на создание item, а затем попытка удаления с пустым токеном")
    def test_create_and_delete_empty_token(self, invalid_item, cleanup_items):
        item_create,item_obj = invalid_item.create_and_delete_empty_token()
        json_item_obj = item_create.json()
        item_id = json_item_obj.get("id")
        cleanup_items.append(item_id)
        assert item_create.status_code == 200, "Получен неожидаемый статус-код "
        assert len(json_item_obj) > 0, "JSON не должен быть пустым"
        assert item_obj.status_code == 401, "Получен неожидаемый статус-код "
        item_json = item_obj.json()
        data = item_json["detail"]
        assert data == "Not authenticated", "Получен неожидаемый текст"
        validate_error401(item_obj, model=Error401,
                          expected_data=item_json)

    @allure.title("Тест на попытку повторного удаления item")
    def test_double_delete_item(self, invalid_item):
        item_obj, delete_item, double_delete = invalid_item.double_delete_item()
        json_item_obj = item_obj.json()
        json_delete_item = delete_item.json()
        json_double_delete = double_delete.json()
        data = json_double_delete["detail"]
        validate_error404(double_delete, model = Error404,
                          expected_data=json_double_delete)
        assert item_obj.status_code == 200, "Получен неожидаемый статус-код "
        assert len(json_item_obj) > 0, "JSON не должен быть пустым"
        assert delete_item.status_code == 200, "Получен неожидаемый статус-код"
        assert len(json_delete_item) > 0, "JSON не должен быть пустым"
        assert double_delete.status_code == 404, "Получен неожидаемый статус-код"
        assert len(json_double_delete) > 0, "JSON не должен быть пустым"
        assert data == "Item not found", "Получен неожидаемый текст"

    @allure.title("Тест на попытку обновления item с несуществующим ID")
    def test_update_unreal_item(self, invalid_item):
        item_obj = invalid_item.update_unreal_item()
        json_item_obj = item_obj.json()
        validate_error422(item_obj, model=Error422,
                          expected_data=json_item_obj)
        assert item_obj.status_code == 422, "Получен неожидаемый статус-код "
        data = json_item_obj["detail"][0]["type"]
        assert data == "uuid_parsing", "Получен неожидаемый текст"
        assert len(json_item_obj) > 0, "Ответ не должен быть пустым"

    @allure.title("Тест на попытку удаления item с несуществующим ID")
    def test_delete_unreal_item(self, invalid_item):
        item_obj = invalid_item.delete_unreal_item()
        json_item_obj = item_obj.json()
        validate_error422(item_obj, model=Error422,
                          expected_data=json_item_obj)
        assert item_obj.status_code == 422, "Получен неожидаемый статус-код "
        data = json_item_obj["detail"][0]["type"]
        assert data == "uuid_parsing", "Получен неожидаемый текст"
        assert len(json_item_obj) > 0, "Ответ не должен быть пустым"
