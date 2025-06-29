import pytest
from utils.test_data_generators import generate_email, generate_password, generate_age, generate_symbol
from utils.test_helpers import assert_auth_response_structure, assert_validation_error_structure
from client.endpoints.auth import AuthEndpoint

@pytest.fixture
def auth_endpoint(client):
    return AuthEndpoint(client)

@pytest.mark.parametrize("email,password,age,expected_status_code", [
    # Правильные данные
    ("random_email", "random_password", "random_age", 200),
    
    # Тесты возраста
    ("random_email", "random_password", "age_0", 200), #Баг, 0 воспринимается как null/None
    ("random_email", "random_password", "age_99", 200),
    ("random_email", "random_password", "age_100", 422),
    ("random_email", "random_password", "age_negative", 422),
    ("random_email", "random_password", "age_letters", 422),
    
    # Тесты email
    ("email_5_chars", "random_password", "random_age", 200),
    ("email_4_chars", "random_password", "random_age", 422),
    ("email_with_spaces", "random_password", "random_age", 422), 
    ("email_special_char", "random_password", "random_age", 422),
    ("email_50_chars", "random_password", "random_age", 200),
    ("email_51_chars", "random_password", "random_age", 422),
    
    # Тесты пароля
    ("random_email", "password_4_chars", "random_age", 422),
    ("random_email", "password_5_chars", "random_age", 200), 
    ("random_email", "password_20_chars", "random_age", 200),
    ("random_email", "password_21_chars", "random_age", 422),
    
    # Пустые поля
    ("", "random_password", "random_age", 422),
    ("random_email", "", "random_age", 422),
    ("random_email", "random_password", "", 422),
    
    # Явная передача null (None)
    ("null_email", "random_password", "random_age", 422),
    ("random_email", "null_password", "random_age", 422),
    ("random_email", "random_password", "null_age", 422),
    
    # SQL инъекции
    ("sql_injection_email", "random_password", "random_age", 422),
    ("random_email", "sql_injection_password", "random_age", 422),
    
    # Существующий аккаунт
    ("existing_email", "random_password", "random_age", 422),
])

def test_api_registration(auth_endpoint, email, password, age, expected_status_code, api_username):

    match email:
        case "random_email":
            email = generate_email()
        case "email_5_chars":
            email = f"{generate_symbol()}@{generate_symbol()}.r"
        case "email_4_chars":
            email = f"{generate_symbol()}@{generate_symbol()}."
        case "email_with_spaces":
            email = f" {generate_email()} "
        case "email_special_char":
            email = "test@example#com"
        case "email_50_chars":
            email = generate_symbol() * 38 + "@example.com"
        case "email_51_chars":
            email = generate_symbol() * 39 + "@example.com"
        case "sql_injection_email":
            email = "'; DROP TABLE users; --"
        case "existing_email":
            email = api_username
        case "null_email":
            email = None
        case _:
            pass
    
    match password:
        case "random_password":
            password = generate_password()
        case "password_4_chars":
            password = generate_password(4)
        case "password_5_chars":
            password = generate_password(5)
        case "password_20_chars":
            password = generate_password(20)
        case "password_21_chars":
            password = generate_password(21)
        case "sql_injection_password":
            password = "'; DROP TABLE users; --"
        case "null_password":
            password = None
        case _:
            pass
    
    match age:
        case "random_age":
            age = generate_age()
        case "age_0":
            age = 0
        case "age_99":
            age = 99
        case "age_100":
            age = 100
        case "age_negative":
            age = -1
        case "age_letters":
            age = "abc"
        case "null_age":
            age = None
        case _:
            pass
    
    response = auth_endpoint.register(email, password, age)
    
    if expected_status_code == 200:
        assert_auth_response_structure(response, email, age)
    else:
        if "body" in response:
            body = response["body"]
        else:
            body = response
        
        if "type" in body and body["type"] == "validation":
            
            if email == "" or email is None:
                assert_validation_error_structure(response, "email")
            elif password == "" or password is None:
                assert_validation_error_structure(response, "password")
            elif age == "" or age is None:
                assert_validation_error_structure(response, "age")
            else:
                assert_validation_error_structure(response)
        else:
            # Проверяем случай с существующим email
            if "fields" in body and "email" in body["fields"]:
                assert "Пользователь с таким email уже существует" in body["fields"]["email"]
            else:
                assert "password" in body["fields"]
                assert "Неправильный логин или пароль" in body["fields"]["password"]

@pytest.mark.parametrize("email,password,expected_status_code", [
    ("api_username", "api_password", 200),
    ("api_username", "wrong_password", 422),
    ("not_register", "any_password", 422),
    ("", "any_password", 422),
    ("api_username", "", 422),
    ("'; DROP TABLE users; --", "any_password", 422),
    ("api_username", "'; DROP TABLE users; --", 422),
    ("api_username_trim", "api_password", 422),
    ("null_email", "api_password", 422),
    ("api_username", "null_password", 422),
])

def test_api_login(auth_endpoint, api_username, api_password, email, password, expected_status_code):

    match email:
        case "api_username":
            email = api_username
        case "api_username_trim":
            email = f" {api_username} "
        case "not_register":
            email = generate_email()
        case "null_email":
            email = None
        case _:
            pass
    
    match password:
        case "api_password":
            password = api_password
        case "wrong_password" | "any_password":
            password = generate_password()
        case "null_password":
            password = None
        case _:
            pass
    
    response = auth_endpoint.login(email, password)
    
    if expected_status_code == 200:
        assert_auth_response_structure(response, email)
    else:
        
        if "body" in response:
            body = response["body"]
        else:
            body = response
        
        if "type" in body and body["type"] == "validation":
            assert_validation_error_structure(response, "email" if email == "" else "password")
        else:
            assert "password" in body["fields"]
            assert "Неправильный логин или пароль" in body["fields"]["password"]