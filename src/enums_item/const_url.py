from enum import Enum
import os
from dotenv import load_dotenv

load_dotenv()

class ConstURL(Enum):
    BASE_URL = "https://dashboard.fast-api.senior-pomidorov.ru/"
    ITEMS_URL = f"https://api.fast-api.senior-pomidorov.ru/api/v1/items/"
    LOGIN_URL = f"https://api.fast-api.senior-pomidorov.ru/api/v1/login/access-token"

class AuthHeaders(Enum):
    AUTH_HEADERS = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }

    AUTH_DATA = {
        "username": os.getenv("VALID_USERNAME"),
        "password": os.getenv("VALID_PASSWORD"),
        "grant_type": "password",
        "scope": "",
        "client_id": "",
        "client_secret": ""
    }

    WRONG_AUTH_DATA = {
        "username": os.getenv("INVALID_USERNAME"),
        "password": os.getenv("INVALID_PASSWORD"),
        "grant_type": "password",
        "scope": "",
        "client_id": "",
        "client_secret": ""
    }

class ApiHeaders(Enum):
    API_HEADERS = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }


