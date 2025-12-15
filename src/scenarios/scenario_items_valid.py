import requests
import allure
from PythonProject5.src.api.api_items import ItemsApi
from PythonProject5.src.item_models.data_model_items import RequestItem

class ItemScenarios:
    def __init__(self, token_session, api_client: ItemsApi):
        self.token_session = token_session
        self.api_client = api_client
        self.generate_dates = RequestItem

    @allure.title("Создание, проверка ID  item ")
    def create_check_item(self):
        ''' Сценарий: создание итем, проверка ID созданного итем,'''
        # 1. Creating item
        with allure.step("Создание item"):
            response = self.api_client.create_item()
            allure.attach(str(response), name="Полученный item", attachment_type=allure.attachment_type.JSON)
        with ((allure.step("Получение ID созданного item"))):
            item_json = response.json()
            id_item = item_json.get("id")
            allure.attach(str(id_item), name="ID созданного item", attachment_type=allure.attachment_type.TEXT)

        #2 Check item creating
        with allure.step("Проверяем что ID не None"):
            if id_item is None:
                raise RuntimeError ("Не удачное получение созданного item")
        return response

    @allure.title("Создание, проверка ID и удаление item ")
    def create_check_delete_item(self):
        ''' Сценарий: создание итем, проверка ID созданного итем,
        затем удаление этого итем '''
        # 1. Creating item
        with allure.step("Создание item"):
            response = self.api_client.create_item()
            allure.attach(str(response), name="Полученный item", attachment_type=allure.attachment_type.JSON)
        with ((allure.step("Получение ID созданного item"))):
            item_json = response.json()
            id_item = item_json.get("id")
            allure.attach(str(id_item), name="ID созданного item", attachment_type=allure.attachment_type.TEXT)

        # 2 Check item creating
        with allure.step("Проверяем что ID не None"):
            if id_item is None:
                raise RuntimeError("Не удачное получение созданного item")

        #3 Deleting item
        with allure.step("Удаление item"):
            delete_item = self.api_client.delete_item(id_item)
            allure.attach(str(delete_item), name="Результат удаления item", attachment_type=allure.attachment_type.TEXT)
        return response, delete_item

    @allure.title("Создание, проверка ID и обновление item ")
    def create_check_update_item(self):
        ''' Сценарий: создание итем, проверка ID созданного итем,
        затем обновление итем '''
        # 1. Creating item
        with allure.step("Создание item"):
            item_create = self.api_client.create_item()
            allure.attach(str(item_create), name="Полученный item", attachment_type=allure.attachment_type.JSON)
        with allure.step("Получение ID созданного item"):
            item_json = item_create.json()
            id_item = item_json.get("id")
            allure.attach(str(id_item), name="ID созданного item", attachment_type=allure.attachment_type.TEXT)

        #2 Check item creating
        with allure.step("Проверяем что ID не None"):
            if id_item is None:
                raise RuntimeError ("Не удачное получение созданного item")

        #3 Updating item
        with allure.step("Обновляем item"):
            update_item = self.api_client.update_item(id_item)
            allure.attach(str(update_item), name="Результат обновления item", attachment_type=allure.attachment_type.JSON)
        return item_create, update_item

    @allure.title("Создание, проверка ID и получение этого item ")
    def create_check_get_item (self):
        ''' Сценарий: Создание итем, проверка ID созданного итем,
        затем получение итем по ID '''
        # 1. Creating item
        with allure.step("Создание item"):
            item_create = self.api_client.create_item()
            allure.attach(str(item_create), name="Полученный item", attachment_type=allure.attachment_type.JSON)
        with allure.step("Получение ID созданного item"):
            item_json = item_create.json()
            id_item = item_json.get("id")
            allure.attach(str(id_item), name="ID созданного item", attachment_type=allure.attachment_type.TEXT)

        # 2 Check item creating
        with allure.step("Проверяем что ID не None"):
            if id_item is None:
                raise RuntimeError("Не удачное получение созданного item")

        #3 Get item
        with allure.step("Получаем item по заданному ID"):
            get_item = self.api_client.get_item(id_item)
            allure.attach(str(get_item), name="Результат получения item по ID", attachment_type=allure.attachment_type.JSON)
        return item_create, get_item

    @allure.title("Создание item, получение с дефолтными параметрами всех items, "
                  "проверка наличия item в списке items")
    def create_check_in_all_items(self):
        """Сценарий: создание итем, затем проверка наличия
        созданного итем в общем списке """
        # 1. Creating item
        with allure.step("Создание item"):
            item_create = self.api_client.create_item()
            allure.attach(str(item_create), name="Полученный item", attachment_type=allure.attachment_type.JSON)
        with allure.step("Получение ID созданного item"):
            item_json = item_create.json()
            id_item = item_json.get("id")
            allure.attach(str(id_item), name="ID созданного item", attachment_type=allure.attachment_type.TEXT)

        #2 Get items
        with allure.step("Получаем список по дефолтгым параметрам"):
            items_all = self.api_client.get_all_items()
            items = items_all.json()
            allure.attach(str(items), name="Полученный список всех items", attachment_type=allure.attachment_type.JSON)
        with allure.step("Проверяем что ID не None"):
            if item_json not in items['data']:
                raise RuntimeError("Отсутствие созданного item в полученном списке")
        return item_create, items_all

    @allure.title("Одновременное создание 10 items")
    def create_multiple_items(self, count: int = 10):
        """ Создает заданное количество сущностей (задано = 10).
        Возвращает список созданных сущностей."""
        # 1. Creating 20 items
        with allure.step("Создаем сразу несколько items"):
            items_responses = []
            allure.attach(str(items_responses), name="Список созданных items",
                          attachment_type = allure.attachment_type.TEXT)
            for _ in range(count):
                try:
                    created_item = self.api_client.create_item()
                    allure.attach(str(created_item),name="Созданный item",
                                  attachment_type=allure.attachment_type.JSON)
                    items_responses.append(created_item)
                except Exception as e:
                    print(f"Ошибка при создании items: {e}")
            allure.attach(str(items_responses), name="Eще раз - Список созданных items",
                          attachment_type=allure.attachment_type.TEXT)
            return items_responses

    @allure.title("Получение items по недефолтным валидным параметрам")
    def filter_items(self):
        """ Сценарий: получить количество итемов по заданными параметрам """
        with allure.step("Получаем недефолтные валидные параметры для запроса"):
            params = RequestItem.params_valid()
        with allure.step("Отправляем запрос на получение списка по заданным параметрам"):
            items = self.api_client.get_all_items(params=params)
        data = items.json().get("data", [])
        skip_value = params.get("skip")
        limit_value = params.get("limit")
        expected_count = limit_value #- skip_value
        return items, data, expected_count