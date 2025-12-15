from PythonProject5.src.item_models.data_error_model import Error422, Error400
from PythonProject5.src.utils_item.validator_error_items import validate_error422, validate_error400

class TestInvalidLogin:
    def test_wrong_create_token(self, login_scenarios):
        login = login_scenarios.wrong_create_token()
        login_json = login.json()
        validate_error422(login, model=Error422,
                          expected_data=login_json)
        assert login.status_code == 422, "Не ожидаемый статус-код"
        data = login_json["detail"][0]["type"]
        assert data == "string_pattern_mismatch", "Получен неожидаемый текст"
        assert len(login_json) > 0, "Ответ не должен быть пустым"

    def test_auth_wrong_data(self, login_scenarios):
        login = login_scenarios.auth_wrong_data()
        login_json = login.json()
        validate_error400(login, model=Error400,
                          expected_data=login_json)
        assert login.status_code == 400, "Не ожидаемый статус-код"
        data = login_json["detail"]
        assert data == "Incorrect email or password", "Получен неожидаемый текст"
        assert len(login_json) > 0, "Ответ не должен быть пустым"

    def test_empty_auth_data(self, login_scenarios):
        login = login_scenarios.empty_auth_data()
        login_json = login.json()
        validate_error400(login, model=Error400,
                          expected_data=login_json)
        assert login.status_code == 400, "Не ожидаемый статус-код"
        data = login_json["detail"]
        assert data == "Incorrect email or password", "Получен неожидаемый текст"
        assert len(login_json) > 0, "Ответ не должен быть пустым"

    def test_non_auth_data(self, login_scenarios):
        login = login_scenarios.non_auth_data()
        login_json = login.json()
        validate_error422(login, model=Error422,
                          expected_data=login_json)
        assert login.status_code == 422, "Не ожидаемый статус-код"
        data = login_json["detail"][0]["type"]
        assert data == "missing", "Получен неожидаемый текст"
        assert len(login_json) > 0, "Ответ не должен быть пустым"
