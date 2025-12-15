import allure
from PythonProject5.src.item_models.data_model_items import ResponseItem, ResponseAllItems, ResponseDeleteItems
from PythonProject5.src.utils_item.validator_item_data import validate_item
from PythonProject5.src.utils_item.validator_all_items import validate_items
from PythonProject5.src.utils_item.validator_item_data import validate_delete_item

class TestValid:

    @allure.title("Тест на создание item")
    def test_create_check_item(self, valid_scenarios, cleanup_items):
        item_obj = valid_scenarios.create_check_item()
        json_item_obj = item_obj.json()
        item_id = json_item_obj.get("id")
        validate_item(item_obj, model=ResponseItem,
                      expected_data=json_item_obj)  # здесь в expected_data= помещаем json_item_obj как ожидаемые данные
        cleanup_items.append(item_id)
        assert item_obj.status_code == 200, "Получен неожидаемый статус-код "
        assert len(json_item_obj) > 0, "JSON не должен быть пустым"
        assert json_item_obj.get("title") not in (None, ""), "Значение ключа 'title' пустое"
        assert item_id not in (None, ""), "Значение ключа 'id' пустое"
        assert json_item_obj.get("owner_id") not in (None, ""), "Значение ключа 'owner_id' пустое"

    @allure.title("Тест на создание и удаление item")
    def test_create_delete_item(self, valid_scenarios):
        item_obj, delete_item = valid_scenarios.create_check_delete_item()
        json_item_obj = item_obj.json()
        item_id = json_item_obj.get("id")
        json_delete_item = delete_item.json()
        validate_delete_item(delete_item, model=ResponseDeleteItems,
                      expected_data=json_delete_item)
        data = json_delete_item["message"]
        assert item_obj.status_code == 200, "Получен неожидаемый статус-код "
        assert len(json_item_obj) > 0, "JSON не должен быть пустым"
        assert json_item_obj.get("title") not in (None, ""), "Значение ключа 'title' пустое"
        assert item_id not in (None, ""), "Значение ключа 'id' пустое"
        assert json_item_obj.get("owner_id") not in (None, ""), "Значение ключа 'owner_id' пустое"
        assert delete_item.status_code == 200, "Получен неожидаемый статус-код"
        assert len(json_delete_item) > 0, "JSON не должен быть пустым"
        assert data == "Item deleted successfully", "Несоответствие в тексте ответа"

    @allure.title("Тест на создание и обновление item")
    def test_create_check_update_item(self,valid_scenarios, cleanup_items):
        obj1, obj2 = valid_scenarios.create_check_update_item()
        print(obj1.json())
        print(obj2.json())
        json_obj1 = obj1.json()
        json_obj2 = obj2.json()
        item_id = json_obj2.get("id")
        validate_item(obj2, model=ResponseItem,
                      expected_data=json_obj2)  # здесь в expected_data= помещаем json_item_obj как ожидаемые данные
        cleanup_items.append(item_id)
        assert json_obj1["title"] != json_obj2["title"], "Значение ключа 'title' не изменилось"
        assert json_obj1["description"] != json_obj2["description"], "Значение ключа 'description' не изменилось"
        assert obj1.status_code == 200, "Получен неожидаемый статус-код "
        assert obj2.status_code == 200, "Получен неожидаемый статус-код "
        assert len(json_obj2) > 0, "JSON не должен быть пустым"
        assert json_obj2.get("title") not in (None, ""), "Значение ключа 'title' пустое"
        assert item_id not in (None, ""), "Значение ключа 'id' пустое"
        assert json_obj2.get("owner_id") not in (None, ""), "Значение ключа 'owner_id' пустое"

    @allure.title("Тест на создание и получение созданного item")
    def test_create_check_get_item(self, valid_scenarios, cleanup_items):
        obj1, obj2 = valid_scenarios.create_check_get_item()
        json_obj1 = obj1.json()
        json_obj2 = obj2.json()
        item_id = json_obj2.get("id")
        validate_item(obj2, model=ResponseItem,
                      expected_data=json_obj2)  # здесь в expected_data= помещаем json_item_obj как ожидаемые данные
        cleanup_items.append(item_id)
        assert json_obj1 == json_obj2, "Тело item различается"
        assert obj1.status_code == 200, "Получен неожидаемый статус-код "
        assert obj2.status_code == 200, "Получен неожидаемый статус-код "
        assert len(json_obj2) > 0, "JSON не должен быть пустым"
        assert json_obj2.get("title") not in (None, ""), "Значение ключа 'title' пустое"
        assert item_id not in (None, ""), "Значение ключа 'id' пустое"
        assert json_obj2.get("owner_id") not in (None, ""), "Значение ключа 'owner_id' пустое"

    @allure.title("Тест на получение общего списка")
    def test_check_all_items(self, valid_scenarios):
        item_create, items = valid_scenarios.create_check_in_all_items()
        json_items = items.json()
        validate_items(items, model=ResponseAllItems, expected_data=json_items)
        assert items.status_code == 200, "Получен неожидаемый статус-код "
        assert len(json_items) > 0, "JSON не должен быть пустым"
        assert len(json_items.get("data")) == json_items.get("count"), "Несоответствие количества data и count"
        assert len(json_items.get("data")) and json_items.get("count") != 0, "Полученный объект пуст"

    @allure.title("Тест на создание item, и проверка его нахождения в общем списке")
    def test_create_check_in_all_items(self, valid_scenarios, cleanup_items):
        item_create, items = valid_scenarios.create_check_in_all_items()
        json_item_create = item_create.json()
        json_items = items.json()
        item_id = json_item_create.get("id")
        validate_items(items, model=ResponseAllItems, expected_data=json_items)
        cleanup_items.append(item_id)
        assert item_create.status_code == 200, "Получен неожидаемый статус-код "
        assert items.status_code == 200, "Получен неожидаемый статус-код "
        assert len(json_items) > 0, "JSON не должен быть пустым"
        assert len(json_items.get("data")) == json_items.get("count"), "Несоответствие количества data и count"
        assert len(json_items.get("data")) and json_items.get("count") != 0, "Полученный объект пуст"
        assert json_item_create in json_items['data'], "созданного item нет в общем списке"

    @allure.title("Тест на одновременное создание нескольких items")
    def test_create_multiple_items(self, valid_scenarios, cleanup_items):
        multiple = 15
        items_responses = valid_scenarios.create_multiple_items(count=multiple)
        assert len(items_responses) == multiple, f'Создано {len(items_responses)} элементов вместо ожидаемого количества'
        json_items = [obj.json() for obj in items_responses]
        items_ids = [item.get("id") for item in json_items]
        assert len(set(items_ids)) == len(items_ids), 'Некоторые созданные элементы имеют одинаковые ID'
        for response_obj in items_responses:
            validate_item(response_obj, model=ResponseItem,
                          expected_data=response_obj.json())
        for item_id in items_ids:
            cleanup_items.append(item_id)
        assert all(response.status_code == 200 for response in items_responses), "Получен неожидаемый статус-код"
        assert all(len(json_item) > 0 for json_item in json_items), "JSON не должен быть пустым"
        assert all(json_item.get("title") not in (None, "") for json_item in json_items) , "Значение ключа 'title' пустое"
        assert all(item_id not in (None, "") for item_id in items_ids), "Значение ключа 'id' пустое"
        assert all(json_item.get("owner_id") not in (None, "") for json_item in json_items) , "Значение ключа 'owner_id' пустое"

    @allure.title("Тест на получение items по недефолтным валидным параметрам")
    def test_filter_items(self, valid_scenarios):
        items_responses, data, expected_count = valid_scenarios.filter_items()
        json_items=items_responses.json()
        validate_items(items_responses, model=ResponseAllItems, expected_data=json_items)
        assert len(data) <= expected_count, f'Получено {len(data)} элементов вместо ожидаемого количества'
        assert items_responses.status_code == 200, "Получен неожидаемый статус-код"