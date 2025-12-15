import allure
from PythonProject5.src.enums_item.const_url import ConstURL
from PythonProject5.src.enums_item.invalid_data import WrongUUID
from PythonProject5.src.item_models.data_model_items import AuthData,RequestItem, WrongRequestItems, NoneItems
from PythonProject5.src.api.api_items import ItemsApi

class BadScenarioCreate:
    def __init__(self,item_session):
        self.session = item_session
        self.base_url = ConstURL.ITEMS_URL.value
        self.token =  AuthData().auth_token()
        self.data_generator = RequestItem
        self.wrong_data = WrongRequestItems
        self.non_data = NoneItems

    @allure.title("Попытка создания item с title более 255 символов")
    def create_too_long_title (self):
        """Создание слишком длинного item"""
        with allure.step("Получаем токен"):
            token_item = self.token
            allure.attach(str(token_item),name="Полученный токен", attachment_type=allure.attachment_type.TEXT)
        with allure.step("Получение данных длиннее > 255 символов"):
            item_create = self.wrong_data.too_long_data()
            allure.attach(str(item_create), name="Полученные данные длинной > 255 символов", attachment_type=allure.attachment_type.TEXT)
        with allure.step("Попытка получения item"):
            response = self.session.post(f'{self.base_url}',
                                     headers=token_item.headers,
                                     json=item_create)
            allure.attach(str(response), name="Ответ на попытку получить item", attachment_type=allure.attachment_type.TEXT)
        return response

    @allure.title("Попытка создания item с пустым title")
    def create_non_title(self):
        """Запрос на создание item без содержания title"""
        with allure.step("Получаем токен"):
            token_item = self.token
            allure.attach(str(token_item), name="Полученный токен", attachment_type=allure.attachment_type.TEXT)
        with allure.step("Получение данных с пустым title"):
            item_create = self.non_data.none_item_data()
            allure.attach(str(item_create), name="Полученные данные c пустым title", attachment_type=allure.attachment_type.TEXT)
        with allure.step("Попытка получения item"):
            response = self.session.post(f'{self.base_url}',
                                     headers=token_item.headers,
                                     json=item_create)
        allure.attach(str(response), name="Ответ на попытку получить item", attachment_type=allure.attachment_type.TEXT)
        return response

    @allure.title("Попытка создания item без токена")
    def create_empty_token(self):
        """Запрос на создание item"""
        with allure.step("Получение токена"):
            token_item = self.token
            allure.attach(str(token_item),name="Полученный токен", attachment_type=allure.attachment_type.TEXT)
        with allure.step("Убираем из header значение 'Authorization'"):
            token_item.headers['Authorization'] = None
            allure.attach(str(token_item.headers), name="Обновленный токен", attachment_type=allure.attachment_type.JSON)
        with allure.step("Получаем данные для создания item"):
            item_create = self.data_generator.item_data()
            allure.attach(str(item_create), name="Полученные данные для создания item",)
        with allure.step("Отправляем запрос на создание item без токена"):
            response = self.session.post(f'{self.base_url}',
                                         headers=token_item.headers,
                                         json=item_create)
            allure.attach(str(response), name="Полученный результат создания item без токена", attachment_type=allure.attachment_type.TEXT)
        return response

class BadScenariosItem:
    def __init__(self, item_session, api_client: ItemsApi):
        self.session = item_session
        self.api_client = api_client
        self.generate_dates = RequestItem
        self.base_url = ConstURL.ITEMS_URL.value
        self.token =  AuthData().auth_token()
        self.empty_token = AuthData().empty_token()
        self.unreal_uuid = WrongUUID.UNREAL_ID.value

    @allure.title("Попытка получения без токена, созданного item")
    def create_and_get_empty_token(self):
        ''' Сценарий: создание итем, проверка ID созданного итем,
        затем удаление этого итем '''
        # 1. Creating valid item
        with allure.step("Создаем item"):
            item_create= self.api_client.create_item()
            allure.attach(str(item_create), name="Полученный item",
                          attachment_type=allure.attachment_type.TEXT)
        with allure.step("Забираем ID созданного item"):
            json_item = item_create.json()
            id_item = json_item.get("id")
            allure.attach(str(id_item), name="ID", attachment_type=allure.attachment_type.TEXT)

        #2 Get item with empty token
        with allure.step("Получаем пустой токен"):
            empty_token = self.empty_token
            allure.attach(str(empty_token), name="результат получения пустого токена", attachment_type=allure.attachment_type.TEXT)
        with allure.step("Отправка GET запроса с пустым токеном"):
            response = self.session.get(f'{self.base_url}{id_item}',
                                    headers=empty_token.headers)
            allure.attach(str(response), name="результат GET запроса с пустым токеном", attachment_type=allure.attachment_type.JSON)
        return item_create, response

    @allure.title("Попытка обновления без токена, созданного item")
    def create_and_update_empty_token(self):
        '''
        Сценарий: создание итем, проверка ID созданного итем,
        затем удаление этого итем '''
        # 1. Creating valid item
        with allure.step("Создаем item"):
            item_create = self.api_client.create_item()
            allure.attach(str(item_create), name="Полученный item",
                          attachment_type=allure.attachment_type.TEXT)
        with allure.step("Забираем ID созданного item"):
            json_item = item_create.json()
            id_item = json_item.get("id")
            allure.attach(str(id_item), name="ID", attachment_type=allure.attachment_type.TEXT)

        #2 Update item with empty token
        with allure.step("Получаем пустой токен"):
            empty_token = self.empty_token
            allure.attach(str(empty_token), name="Результат получения пустого токена", attachment_type=allure.attachment_type.TEXT)
        with allure.step("Получаем данные для обновления item"):
            item_update = self.generate_dates.update_item_data()
            allure.attach(str(item_update), name="Результат получения данных для обновления item")
        with allure.step("Отравляем запрос c пустым токен на обновление item"):
            response = self.session.put(f'{self.base_url}{id_item}',
                                         headers=empty_token.headers,
                                         json=item_update)
            allure.attach(str(response), name="Результат запроса c пустым токен на обновление item", attachment_type=allure.attachment_type.JSON)
        return item_create, response

    def create_and_delete_empty_token(self):
        '''
        Сценарий: создание итем, проверка ID созданного итем,
        затем удаление этого итем '''
        # 1. Creating valid item
        with allure.step("Создаем item"):
            item_create = self.api_client.create_item()
            allure.attach(str(item_create), name="Полученный item",
                          attachment_type=allure.attachment_type.TEXT)
        with allure.step("Забираем ID созданного item"):
            json_item = item_create.json()
            id_item = json_item.get("id")
            allure.attach(str(id_item), name="ID", attachment_type=allure.attachment_type.TEXT)

        #2 Delete item with empty token
        with allure.step("Получаем пустой токен"):
            empty_token = self.empty_token
            allure.attach(str(empty_token), name="результат получения пустого токена", attachment_type=allure.attachment_type.TEXT)
        with allure.step("Отправка DELETE запроса с пустым токеном"):
            response = self.session.delete(f'{self.base_url}{id_item}',
                                    headers=empty_token.headers)
            allure.attach(str(response), name="результат DELETE запроса с пустым токеном", attachment_type=allure.attachment_type.JSON)
        return item_create, response

    @allure.title("Попытка повторного удаления item")
    def double_delete_item(self):
        ''' Сценарий: создание итем, удаление итем,
        затем попытка повторно удалить итем '''
        # 1. Creating valid item
        with allure.step("Создаем item"):
            item_create = self.api_client.create_item()
            allure.attach(str(item_create), name="Полученный item",
                          attachment_type=allure.attachment_type.JSON)
        with allure.step("Забираем ID созданного item"):
            json_item = item_create.json()
            id_item = json_item.get("id")
            allure.attach(str(id_item), name="ID", attachment_type=allure.attachment_type.TEXT)

        #2 Deleting item
        with allure.step("Отправляем DELETE запрос "):
            response = self.api_client.delete_item(id_item)
            allure.attach(str(response), name="Результат удаления item", attachment_type=allure.attachment_type.JSON)

        # 3 Deleting item one more
        with allure.step("Получаем токен для повторного DELETE запроса"):
            token_item = self.token
            allure.attach(str(token_item),name="Результат удаления item", attachment_type=allure.attachment_type.JSON)
        with allure.step("Отправляем ПОВТРОНЫЙ DELETE запрос"):
            double_response = self.session.delete(f'{self.base_url}{id_item}', # используем редактированный запрос из модуля api_items.py т.к. метод api_client.delete_item содержит
                                       headers=token_item.headers)             # raise for status из-за которого запрос падает с исключением requests.exceptions.HTTPError: 404 Client Error
            allure.attach(str(double_response), name="Результат повторного удаления item", attachment_type=allure.attachment_type.JSON)
        double_del_item = double_response.json()
        return item_create, response, double_response

    @allure.title("Попытка обновления item c несуществующим токеном")
    def update_unreal_item(self):
        ''' Сценарий: создание итем,
        затем обновление итем с несуществующим ID'''
        # 1 Updating item with wrong ID
        with allure.step("Получаем токен для PUT запроса"):
            token_item = self.token
            allure.attach(str(token_item), name="Результат получения токена для PUT запроса",
                          attachment_type=allure.attachment_type.TEXT)
        with allure.step("Получаем несуществующий ID"):
            unreal_id = self.unreal_uuid
            allure.attach(str(unreal_id), name="Результат получения несуществующего ID",
                          attachment_type=allure.attachment_type.TEXT)
        with allure.step("Получаем валидные данные для обновления item"):
            item_update = self.generate_dates.update_item_data()
            allure.attach(str(item_update), name="Результат получения данных для обновления item",
                          attachment_type=allure.attachment_type.TEXT)
        with allure.step("Отправка PUT запроса с несуществующим ID"):
            response = self.session.put(f'{self.base_url}{unreal_id}',
                                         headers=token_item.headers,
                                         json=item_update)
            allure.attach(str(response), name="Результат отправки PUT запроса с несуществующим ID",
                          attachment_type=allure.attachment_type.TEXT)
        unreal_item = response.text
        return response

    def delete_unreal_item(self):
        '''
        Сценарий: создание итем,
        затем удалить итем с несуществующим ID'''
        # 1. Deleting item with wrong ID
        with allure.step("Получаем токен для PUT запроса"):
            token_item = self.token
            allure.attach(str(token_item), name="Результат получения токена для PUT запроса",
                          attachment_type=allure.attachment_type.TEXT)
        with allure.step("Получаем несуществующий ID"):
            unreal_id = self.unreal_uuid
            allure.attach(str(unreal_id), name="Результат получения несуществующего ID",
                          attachment_type=allure.attachment_type.TEXT)
        with allure.step("Отправка DELETE запроса с несуществующим ID"):
            response = self.session.delete(f'{self.base_url}{unreal_id}',
                                        headers=token_item.headers)
            allure.attach(str(response), name="Результат отправки DELETE запроса с несуществующим ID",
                          attachment_type=allure.attachment_type.TEXT)
        unreal_item = response.text
        return response