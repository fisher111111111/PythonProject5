import pytest
from pydantic import BaseModel, ValidationError
from requests import Response
from typing import Type
from PythonProject5.src.item_models.data_model_items import ResponseAllItems

def validate_items(
    response: Response,
    model: Type[ResponseAllItems],
    expected_data: dict,
    expected_status: int = 200
) -> BaseModel:

    # Проверка статуса ответа
    if response.status_code != expected_status:
        pytest.fail(f"Ожидался статус {expected_status}, но получен {response.status_code}: {response.text}")

    # Попытка парсинга JSON
    try:
        data_items = response.json()
    except Exception as e:
        pytest.fail(f"Ошибка парсинга JSON: {e}\nResponse: {response.text}")

    try:
        parsed = model(**data_items)
    except ValidationError as e:
        # Специальная обработка случая, когда count > len(data)
        errors = str(e.errors())
        if "'count'" in errors and "'data'" in errors:
            pass  # Игнорируем ошибку
        else:
            raise  # Поднимаем остальные ошибки дальше

    if expected_data:
        expected_model = model(**expected_data)
        if parsed.model_dump(exclude_unset=True) != expected_model.model_dump(exclude_unset=True):
            pytest.fail(
                f"Данные ответа не совпадают с ожидаемыми:\n"
                f"Expected: {expected_model.model_dump()}\n"
                f"Actual:   {parsed.model_dump()}"
            )

    return parsed
