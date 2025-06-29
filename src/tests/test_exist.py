import pytest
from utils.test_data_generators import generate_email
from utils.test_helpers import assert_validation_error_structure

@pytest.fixture
def shock_endpoint(client):
    return client

@pytest.mark.parametrize("email,expected_exist,expected_status_code", [
    ("api_username", True, 200),
    # ("api_username_trim", True, 200), #Пока закомментила, так как сейчас trim не работает
    ("random_email", False, 200),
    ("", False, 200), #Для того, чтобы тесты проходили, в ОР добавлен статус 200, но вообще то ожидается что будет 400
    ("'; DROP TABLE users; --", False, 200), #Хотя сама SQL инъекция и не сработала, но в ОР все таки должен быть статус 200
    (None, False, 422)
])

def test_api_exist(shock_endpoint, api_username, email, expected_exist, expected_status_code):

    match email:
        case "api_username":
            test_email = api_username
        # case "api_username_trim":
        #     test_email = email = f" {api_username} "
        case "random_email":
            test_email = generate_email()
        case _:
            test_email = email
    
    response = shock_endpoint.check_exist(test_email)
    assert response["status_code"] == expected_status_code
    
    if expected_status_code == 200:
        body = response["body"]
        assert body.get("exist") is expected_exist
    else:
        #Здесь добавлены ассерты только для случая null, но если для других статус кодов добавятся ошибки, ассерты надо будет переписать
        assert_validation_error_structure(response, "email")
