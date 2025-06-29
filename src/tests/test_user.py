import pytest
from utils.test_data_generators import generate_name, generate_symbol
from utils.test_helpers import assert_user_response_structure, assert_validation_error_structure
from src.client.endpoints.user import UserEndpoint

@pytest.fixture
def user_endpoint(client):
    return UserEndpoint(client)

@pytest.mark.parametrize("new_name,expected_status_code", [
    ("random_name", 200),
    ("", 422),
    (None, 422),
    ("'; DROP TABLE users; --", 200),
    ("long_name", 200), 
    ("too_long_name", 422),
    ("random_russian_name", 200),
])

def test_api_name(user_endpoint, api_username, api_password, new_name, expected_status_code):

    match new_name:
        case "random_name":
            new_name = generate_name()
        case "random_russian_name":
            new_name = generate_name(language="ru_RU")
        case "long_name":
            new_name = generate_symbol() * 45
        case "too_long_name":
            new_name = generate_symbol() * 46
        case _:
            pass
    
    response = user_endpoint.change_name(new_name, api_username, api_password)
    
    if expected_status_code == 200:
        assert_user_response_structure(response, api_username)
        if "body" in response:
            user = response["body"]["user"]
        else:
            user = response["user"]
        assert user["name"] == new_name
    else:
        assert_validation_error_structure(response, "name")

def test_api_user(user_endpoint, api_username, api_password):

    response = user_endpoint.get_current_user(api_username, api_password)
    assert_user_response_structure(response, api_username)