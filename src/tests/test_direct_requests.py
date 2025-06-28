from utils.test_data_generators import generate_email, generate_password, generate_name, generate_age

def test_api_available(client):
    """Проверяем, что API доступно и возвращает ожидаемый ответ."""
    response = client.check_health()
    assert response.get("status") == "ok"
    assert isinstance(response.get("timestamp"), str)
    assert response.get("database") == "connected"
    assert isinstance(response.get("uptime"), (int, float))
    assert response.get("environment") == "production"

def test_api_registration(auth_endpoint):
    """Проверяем регистрацию пользователя"""
    registration_data = {
        "email": generate_email(),
        "password": generate_password(),
        "age": generate_age()
    }
    
    response = auth_endpoint.register(
        registration_data["email"],
        registration_data["password"],
        registration_data["age"]
    )
    
    # Проверяем структуру ответа
    assert "token" in response
    assert "user" in response
    
    # Проверяем токен
    assert isinstance(response["token"], str)
    assert len(response["token"]) > 0
    
    # Проверяем данные пользователя
    user = response["user"]
    assert "id" in user
    assert "email" in user
    assert "name" in user
    assert "age" in user
    
    assert isinstance(user["id"], int)
    assert isinstance(user["email"], str)
    assert isinstance(user["name"], str)
    assert isinstance(user["age"], int)

def test_api_login(auth_endpoint, api_username, api_password):
    """Проверяем авторизацию пользователя"""
    response = auth_endpoint.login(api_username, api_password)
    
    # Проверяем структуру ответа
    assert "token" in response
    assert "user" in response
    
    # Проверяем токен
    assert isinstance(response["token"], str)
    assert len(response["token"]) > 0
    
    # Проверяем данные пользователя
    user = response["user"]
    assert "id" in user
    assert "email" in user
    assert "name" in user
    assert "age" in user
    
    assert isinstance(user["id"], int)
    assert isinstance(user["email"], str)
    assert isinstance(user["name"], str)
    assert isinstance(user["age"], int)

def test_api_exist(shock_endpoint, api_username):
    """Проверяем ШОКовость пользователя"""
    response = shock_endpoint.check_exist(api_username)
    assert response.get("exist") is True

def test_api_name(user_endpoint, api_username, api_password):
    """Смена имени для пользователя"""
    new_name = generate_name()
    
    response = user_endpoint.change_name(new_name, api_username, api_password)
    
    print(f"Response: {response}")
    if isinstance(response, dict) and "user" in response:
        print(f"User data: {response['user']}")

def test_api_user(user_endpoint, api_username, api_password):
    """Получение данных о пользователе"""
    response = user_endpoint.get_current_user(api_username, api_password)
    
    print(f"Response: {response}")
    if isinstance(response, dict) and "user" in response:
        print(f"User data: {response['user']}")