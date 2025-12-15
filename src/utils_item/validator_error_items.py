import pytest
from pydantic import BaseModel, ValidationError
from requests import Response
from typing import Type
from PythonProject5.src.item_models.data_error_model import Error401, Error404, Error422, Error400


def validate_error422(
    response: Response,
    model: Type[Error422],
    expected_data: dict,
    expected_status: int = 422
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

def validate_error400(
    response: Response,
    model: Type[Error400],
    expected_data: dict,
    expected_status: int = 400
) -> BaseModel:

    if response.status_code != expected_status:
        pytest.fail(f"Ожидался статус {expected_status}, но получен {response.status_code}: {response.text}")

    try:
        data_item = response.json()
    except Exception as e:
        pytest.fail(f"Ошибка текста: {e}\nResponse: {response.text}")

    try:
        parsed = model(**data_item)
    except ValidationError as e:
        pytest.fail(f"Валидация не прошла:\n{e}")

    if expected_data:
        expected_model = model(**expected_data)
        if parsed.model_dump(exclude_unset=True) != expected_model.model_dump(exclude_unset=True):
            pytest.fail(
                f"Данные ответа не совпадают с ожидаемыми:\n"
                f"Expected: {expected_model.model_dump()}\n"
                f"Actual:   {parsed.model_dump()}"
            )

    return parsed

def validate_error401(
    response: Response,
    model: Type[Error401],
    expected_data: dict,
    expected_status: int = 401
) -> BaseModel:

    if response.status_code != expected_status:
        pytest.fail(f"Ожидался статус {expected_status}, но получен {response.status_code}: {response.text}")

    try:
        data_item = response.json()
    except Exception as e:
        pytest.fail(f"Ошибка текста: {e}\nResponse: {response.text}")

    try:
        parsed = model(**data_item)
    except ValidationError as e:
        pytest.fail(f"Валидация не прошла:\n{e}")

    if expected_data:
        expected_model = model(**expected_data)
        if parsed.model_dump(exclude_unset=True) != expected_model.model_dump(exclude_unset=True):
            pytest.fail(
                f"Данные ответа не совпадают с ожидаемыми:\n"
                f"Expected: {expected_model.model_dump()}\n"
                f"Actual:   {parsed.model_dump()}"
            )

    return parsed

def validate_error404(
    response: Response,
    model: Type[Error404],
    expected_data: dict,
    expected_status: int = 404
) -> BaseModel:

    if response.status_code != expected_status:
        pytest.fail(f"Ожидался статус {expected_status}, но получен {response.status_code}: {response.text}")

    try:
        data_item = response.json()
    except Exception as e:
        pytest.fail(f"Ошибка текста: {e}\nResponse: {response.text}")

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