import os
from dotenv import load_dotenv
from PythonProject5.src.enums_item.const_url import ConstURL, AuthHeaders

load_dotenv()

class AuthLogin:
    def  __init__(self, auth_session):
        self.headers = AuthHeaders.AUTH_HEADERS.value
        self.login = ConstURL.LOGIN_URL.value
        self.auth_session = auth_session

    def create_token(self):
        """Создаем валидные данные для авторизации"""
        auth_data = AuthHeaders.AUTH_DATA.value
        response_token = self.auth_session.post(self.login, headers=self.headers, data=auth_data)
        return response_token

    def wrong_create_token(self):
        """Создаем валидные данные для авторизации без grant_type"""
        auth_data = {
            "username": os.getenv("VALID_USERNAME"),
            "password": os.getenv("VALID_PASSWORD"),
            "grant_type": ""
        }
        response_token = self.auth_session.post(self.login, headers=self.headers, data=auth_data)
        return response_token

    def auth_wrong_data(self):
        """Невалидные данные для авторизации"""
        auth_wrong = {
            "username": os.getenv("INVALID_USERNAME"),
            "password": os.getenv("INVALID_PASSWORD")
        }
        response_token = self.auth_session.post(self.login, headers=self.headers, data=auth_wrong)
        return response_token

    def non_auth_data(self):
        """Отправляет запрос на создание токена аутентификации."""
        none_auth = {
            "username": os.getenv("None"),
            "password": os.getenv("None")
        }
        response_token = self.auth_session.post(self.login, headers=self.headers, data=none_auth)
        return response_token

    def empty_auth_data(self):
        """Отправляет запрос на создание токена аутентификации."""
        empty_auth = {
            "username": "",
            "password": ""
        }
        response_token = self.auth_session.post(self.login, headers=self.headers, data=empty_auth)
        return response_token