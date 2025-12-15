from PythonProject5.src.enums_item.const_url import ConstURL, ApiHeaders
from PythonProject5.src.item_models.data_model_items import AuthData,RequestItem
import allure


class ItemsApi:
    def __init__(self,item_session):
       self.session = item_session
       self.base_url = ConstURL.ITEMS_URL.value
       self.headers = ApiHeaders.API_HEADERS.value
       self.token =  AuthData().auth_token()
       self.data_generator = RequestItem

    @allure.title("Создание нового item")
    def create_item (self):
        """Запрос на создание item"""
        token_item = self.token
        item_create = self.data_generator.item_data()
        response = self.session.post(f'{self.base_url}',
                                     headers=token_item.headers,
                                     json=item_create)
        allure.attach(str(response), name="Результат запроса на создание item", attachment_type=allure.attachment_type.TEXT)
        if response.status_code != 200:
            response.raise_for_status()
        return response

    @allure.title("Получение всех items")
    def get_all_items(self, params = None):
        """Запрос на получение списка всех items"""
        token_item = self.token
        response = self.session.get(f'{self.base_url}', params=params,
                                    headers=token_item.headers)
        allure.attach(str(response), name="Результат запроса на получение всех items",
                      attachment_type=allure.attachment_type.TEXT)
        if response.status_code != 200:
            response.raise_for_status()
        return response

    @allure.title("Получение item")
    def get_item (self, item_id):
        token_item = self.token
        response = self.session.get(f'{self.base_url}{item_id}',
                                    headers=token_item.headers)
        allure.attach(str(response), name="Результат запроса на получение item",
                      attachment_type=allure.attachment_type.TEXT)
        if response.status_code != 200:
            response.raise_for_status()
        return response

    @allure.title("Обновление item")
    def update_item (self, item_id):
        """Запрос на обновление item"""
        token_item = self.token
        item_update = self.data_generator.update_item_data()
        response = self.session.put(f'{self.base_url}{item_id}',
                                     headers=token_item.headers,
                                     json=item_update)
        allure.attach(str(response), name="Результат запроса на обновление item",
                      attachment_type=allure.attachment_type.TEXT)
        if response.status_code != 200:
            response.raise_for_status()
        return response

    @allure.title("Удаление item")
    def delete_item (self, item_id):
        token_item = self.token
        response = self.session.delete(f'{self.base_url}{item_id}',
                                    headers=token_item.headers)
        allure.attach(str(response), name="Результат запроса на удаление item",
                      attachment_type=allure.attachment_type.TEXT)
        if response.status_code != 200:
            response.raise_for_status()
        return response