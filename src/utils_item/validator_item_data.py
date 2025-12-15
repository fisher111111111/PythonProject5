import pytest
from pydantic import BaseModel, ValidationError
from requests import Response
from typing import Type
from PythonProject5.src.item_models.data_model_items import ResponseItem, ResponseDeleteItems, ResponseLogin

def validate_item(
    response: Response,
    model: Type[ResponseItem],
    expected_data: dict,
    expected_status: int = 200
) -> BaseModel:

    if response.status_code != expected_status:
        pytest.fail(f"Ожидался статус {expected_status}, но получен {response.status_code}: {response.text}")

    try:
        data_item = response.json()
    except Exception as e:
        pytest.fail(f"Ошибка парсинга JSON: {e}\nResponse: {response.text}")

    try:
        parsed = model(**data_item)
    except ValidationError as e:
        pytest.fail(f"Pydantic валидация не прошла:\n{e}")

    if expected_data:
        expected_model = model(**expected_data)
        if parsed.model_dump(exclude_unset=True) != expected_model.model_dump(exclude_unset=True):
            pytest.fail(
                f"Данные ответа не совпадают с ожидаемыми:\n"
                f"Expected: {expected_model.model_dump()}\n"
                f"Actual:   {parsed.model_dump()}"
            )

    return parsed

def validate_delete_item(
    response: Response,
    model: Type[ResponseDeleteItems],
    expected_data: dict,
    expected_status: int = 200
) -> BaseModel:

    if response.status_code != expected_status:
        pytest.fail(f"Ожидался статус {expected_status}, но получен {response.status_code}: {response.text}")

    try:
        data_item = response.json()
    except Exception as e:
        pytest.fail(f"Ошибка парсинга JSON: {e}\nResponse: {response.text}")

    try:
        parsed = model(**data_item)
    except ValidationError as e:
        pytest.fail(f"Pydantic валидация не прошла:\n{e}")

    if expected_data:
        expected_model = model(**expected_data)
        if parsed.model_dump(exclude_unset=True) != expected_model.model_dump(exclude_unset=True):
            pytest.fail(
                f"Данные ответа не совпадают с ожидаемыми:\n"
                f"Expected: {expected_model.model_dump()}\n"
                f"Actual:   {parsed.model_dump()}"
            )

    return parsed

def validator_login(
    response: Response,
    model: Type[ResponseLogin],
    expected_data: dict,
    expected_status: int = 200
) -> BaseModel:

    if response.status_code != expected_status:
        pytest.fail(f"Ожидался статус {expected_status}, но получен {response.status_code}: {response.text}")

    try:
        data_item = response.json()
    except Exception as e:
        pytest.fail(f"Ошибка парсинга JSON: {e}\nResponse: {response.text}")

    try:
        parsed = model(**data_item)
    except ValidationError as e:
        pytest.fail(f"Pydantic валидация не прошла:\n{e}")

    if expected_data:
        expected_model = model(**expected_data)
        if parsed.model_dump(exclude_unset=True) != expected_model.model_dump(exclude_unset=True):
            pytest.fail(
                f"Данные ответа не совпадают с ожидаемыми:\n"
                f"Expected: {expected_model.model_dump()}\n"
                f"Actual:   {parsed.model_dump()}"
            )

    return parsed