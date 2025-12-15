import requests
from pydantic import BaseModel
from typing import Optional
import random
import string
from faker import Faker
import os
from dotenv import load_dotenv
import allure
from PythonProject5.src.enums_item.const_url import ConstURL, AuthHeaders

load_dotenv()
fake = Faker('ru_RU')
BASE_URL = ConstURL.BASE_URL.value
LOGIN_URL =  ConstURL.LOGIN_URL.value

"""Класс генерации авторизации"""
class AuthData:
    def auth_item_data(self):
        """Создаем валидные данные для авторизации"""
        return  {"username": os.getenv("VALID_USERNAME"), "password": os.getenv("VALID_PASSWORD")}

    def auth_wrong_data(self):
        """Невалидные данные для авторизации"""
        return  {"username": os.getenv("INVALID_USERNAME"), "password": os.getenv("INVALID_PASSWORD")}

    def auth_header_data(self):
        """Создаем валидные данные для авторизации"""
        return AuthHeaders.AUTH_HEADERS.value

    @staticmethod
    @allure.title("Получение токена для сессии")
    def auth_token():
        """Создание сессию с авторизацией"""
        token_session = requests.Session()
        auth_data = AuthHeaders.AUTH_DATA.value
        auth_headers = AuthHeaders.AUTH_HEADERS.value
        response = (token_session.post(LOGIN_URL,
                                      headers=auth_headers,
                                      data=auth_data))
        allure.attach(str(response), name="Данные для получения токена", attachment_type=allure.attachment_type.JSON)
        response.raise_for_status()
        items_token = response.json()["access_token"]
        token_session.headers.update({"Authorization": f"Bearer {items_token}"})
        return token_session

    @allure.title("Получение токена для сессии")
    def valid_token(self):
        """Создание сессию с авторизацией"""
        token_session = requests.Session()
        auth_data = AuthHeaders.AUTH_DATA.value
        auth_headers = AuthHeaders.AUTH_HEADERS.value
        response = token_session.post(LOGIN_URL,
                                      headers=auth_headers,
                                      data=auth_data)
        allure.attach(str(response), name="Данные для получения токена", attachment_type=allure.attachment_type.JSON)
        response.raise_for_status()
        items_token = response.json()["access_token"]
        token_session.headers.update({"Authorization": f"Bearer {items_token}"})
        token_valid = token_session.headers
        return token_valid

    @allure.title("Создание сессии без токена")
    def empty_token(self):
        """Создание сессию с авторизацией"""
        token_session = requests.Session()
        auth_data = AuthHeaders.AUTH_DATA.value
        auth_headers = AuthHeaders.AUTH_HEADERS.value
        response = token_session.post(LOGIN_URL,
                                      headers=auth_headers,
                                      data=auth_data)
        allure.attach(str(response), name="Данные для получения токена", attachment_type=allure.attachment_type.JSON)
        response.raise_for_status()
        token_session.headers.update({"Authorization": f""})
        return token_session

"""Класс моделей создаваеиых данных"""
class RequestItem (BaseModel):
    title: str
    description: Optional[str] = None

    """ Функции для генерации тестовых данных"""
    @classmethod
    @allure.title("Создание данных для item")
    def item_data(cls) -> "RequestItem":
        '''Генерация данный для создания итем'''
        object_item = cls(
            title=fake.text(max_nb_chars=10),
            description=fake.text(max_nb_chars=random.randint
            (5, 10))
            if random.choice([True, False])
            else None
        )
        allure.attach(str(object_item), name="Данные для создани item", attachment_type=allure.attachment_type.JSON)
        return object_item.model_dump()

    @classmethod
    def update_item_data(cls) -> "RequestItem":
        '''Генерация данных для обновления итем'''
        object_item = cls(
            title=fake.text(max_nb_chars=20),
            description=fake.text(max_nb_chars=random.randint(15, 20)) if random.choice([True, False]) else None
        )
        if object_item.description is None:   # Если description равен None, меняем его на подходящий формат
            object_item.description = ""
        allure.attach(str(object_item), name="Данные для обновления item",
                      attachment_type=allure.attachment_type.JSON)
        return object_item.model_dump()

    @classmethod
    @allure.title("Недефолтные значения параметров GET_items")
    def params_valid(cls):  # далее не стал делать невалидные данные для params, т.к. параметры работают некорректно!!!
        '''Генерация не дефолтных параметров для проверки работоспособности выборки сервера'''
        skip = 0
        allure.attach(str(skip), name="Значение SKIP", attachment_type=allure.attachment_type.JSON)
        limit = random.randint(0, 99)
        allure.attach(str(limit), name="Значение LIMIT", attachment_type=allure.attachment_type.JSON)
        return {"skip": skip, "limit": limit}

"""Классы генерации невалидиных данных"""
class WrongRequestItems(BaseModel):
    '''  генерация данных содержащих более 255 символов
    для значения "title" '''
    title: str
    description: Optional[str] = None

    @classmethod
    @allure.title("Создание title длиннее 255 символов")
    def too_long_data(cls) -> "WrongRequestItems":
        length = random.randint(256, 299)
        letters = string.ascii_letters + string.digits + string.punctuation + ' '
        result = ''.join(random.choices(letters, k=length))
        object_item = cls(
                    title=result,
                    description=fake.text(max_nb_chars=15)
                )
        allure.attach(str(object_item), name="Данные для title > 255 символов", attachment_type=allure.attachment_type.JSON)
        return object_item.model_dump()

class NoneItems(BaseModel):
    ''' генерация данных, где "title" равно None '''
    title: str=""
    description: Optional[str] = None

    @classmethod
    @allure.title("Создание title равного None")
    def none_item_data(cls) -> "NoneItems":
        object_item = cls(
            title= "",
            description=fake.text(max_nb_chars=15)
        )
        allure.attach(str(object_item), name="Данные для item = None", attachment_type=allure.attachment_type.JSON)
        return object_item.model_dump()

"""Класс получаемых данных"""
class ResponseItem (BaseModel):
    title: str
    description: Optional[str] = None
    id: str
    owner_id: str

class ResponseAllItems(BaseModel):
    data: list[ResponseItem]
    count: int

class ResponseDeleteItems (BaseModel):
    message: str = "Item deleted successfully"

class ResponseLogin (BaseModel):
    access_token: str
    token_type: str="bearer"