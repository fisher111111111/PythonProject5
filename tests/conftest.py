import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
import requests
import allure
from PythonProject5.src.utils_item.urls_item import ItemsURLs
from PythonProject5.src.api.api_items import ItemsApi
from PythonProject5.src.scenarios.scenario_items_valid import ItemScenarios
from PythonProject5.src.scenarios.scenario_items_invalid import BadScenariosItem, BadScenarioCreate
from PythonProject5.src.api.login_access import AuthLogin

BASE_URL = ItemsURLs.base_url()
ITEMS = ItemsURLs.items_endpoint()
ITEM = ItemsURLs.items_endpoint_id
LOGIN = ItemsURLs.auth_endpoint()

"""Фикстура для обработки объектов логина"""
@allure.title("Фикстура получения сценариев для логина")
@pytest.fixture(scope="session")
def login_scenarios():
    session = requests.Session()
    api_login = AuthLogin(session)
    return api_login

"""Фикстура для создания объекта класса сценария"""
@allure.title("Фикстура получения валидных сценариев")
@pytest.fixture(scope="session")
def valid_scenarios():
    session = requests.Session()
    api_client = ItemsApi(session)
    scenarios = ItemScenarios(session, api_client)
    return scenarios

@allure.title("Фикстура получения невалидных сценариев получения item")
@pytest.fixture(scope="session")
def invalid_create():
    session = requests.Session()
    scenarios = BadScenarioCreate(session)
    return scenarios

@allure.title("Фикстура получения невалидных сценариев работы с полученным item")
@pytest.fixture(scope="session")
def invalid_item():
    session = requests.Session()
    api_client = ItemsApi(session)
    scenarios = BadScenariosItem(session, api_client)
    return scenarios

@allure.title("Фикстура удаления item")
@pytest.fixture(scope="session")
def cleanup_items():
    session = requests.Session()
    api_client = ItemsApi(session)
    item_ids = []
    yield item_ids  # добавляем id сюда
    for item_id in item_ids: # после теста удаляем все item по id
        delete_response =api_client.delete_item(item_id)
        assert delete_response.status_code == 200
