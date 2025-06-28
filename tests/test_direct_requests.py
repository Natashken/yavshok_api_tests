import requests
from dotenv import load_dotenv
import os
from utils.test_data_generators import generate_email, generate_password, generate_name, generate_age

from urllib3 import response

# Загружаем переменные окружения
load_dotenv()

API_BASE_URL = os.getenv('API_BASE_URL')
API_USERNAME = os.getenv('API_USERNAME')
API_PASSWORD = os.getenv('API_PASSWORD')

# Глобальная переменная для хранения токена, позже надо вынести это в фикстуры
AUTH_TOKEN = None

def test_api_available():
    """Проверяем, что API доступно и возвращает ожидаемый ответ."""
    response = requests.get(f"{API_BASE_URL}/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert isinstance(body["timestamp"], str)
    assert body["database"] == "connected"
    assert isinstance(body["uptime"], (int, float))
    assert body["environment"] == "production"

def test_api_registration():
    """Проверяем регистрацию пользователя"""
    registration_data = {
        "email": generate_email(),
        "password": generate_password(),
        "age": generate_age()
    }
    
    response = requests.post(
        f"{API_BASE_URL}/auth/register",
        json=registration_data
    )
    
    # Проверяем ответ
    assert response.status_code == 200
    body = response.json()
    
    # Проверяем структуру ответа
    assert "token" in body
    assert "user" in body
    
    # Проверяем токен
    assert isinstance(body["token"], str)
    assert len(body["token"]) > 0
    
    # Проверяем данные пользователя
    user = body["user"]
    assert "id" in user
    assert "email" in user
    assert "name" in user
    assert "age" in user
    
    assert isinstance(user["id"], int)
    assert isinstance(user["email"], str)
    assert isinstance(user["name"], str)
    assert isinstance(user["age"], int)

def test_api_login():
    """Проверяем авторизацию пользователя"""
    global AUTH_TOKEN
    
    authorisation_data = {
        "email": API_USERNAME,
        "password": API_PASSWORD
    }
    
    response = requests.post(
        f"{API_BASE_URL}/auth/login",
        json=authorisation_data
    )
    
    # Проверяем ответ
    assert response.status_code == 200
    body = response.json()
    
    # Сохраняем токен для использования в других тестах
    AUTH_TOKEN = body["token"]
    print(f"Token saved: {AUTH_TOKEN[:20]}...")
    
    # Проверяем структуру ответа
    assert "token" in body
    assert "user" in body
    
    # Проверяем токен
    assert isinstance(body["token"], str)
    assert len(body["token"]) > 0
    
    # Проверяем данные пользователя
    user = body["user"]
    assert "id" in user
    assert "email" in user
    assert "name" in user
    assert "age" in user
    
    assert isinstance(user["id"], int)
    assert isinstance(user["email"], str)
    assert isinstance(user["name"], str)
    assert isinstance(user["age"], int)


def test_api_exist():
    """Проверяем ШОКовость пользователя"""
    shock_data = {
        "email": API_USERNAME
    }
    
    response = requests.post(
        f"{API_BASE_URL}/exist",
        json=shock_data
    )
    
    # Проверяем ответ
    assert response.status_code == 200
    body = response.json()
    assert body["exist"] == True


def test_api_name():
    """Смена имени для пользователя"""
    global AUTH_TOKEN
    print(f"Current token: {AUTH_TOKEN}")
    
    if not AUTH_TOKEN:
        print("Token not available, skipping authenticated test")
        return
    
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    
    name_data = {
        "name": generate_name()
    }
    
    print(f"Sending name data: {name_data}")
    print(f"Headers: {headers}")
    
    response = requests.patch(
        f"{API_BASE_URL}/user/name",
        json=name_data,
        headers=headers
    )
    
    print(f"Response status: {response.status_code}")
    print(f"Response headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        body = response.json()
        print(f"Response body: {body}")
    else:
        print(f"Error response: {response.text}")

def test_api_user():
    """Получение данных о пользователе"""
    global AUTH_TOKEN
    print(f"Current token: {AUTH_TOKEN}")
    
    if not AUTH_TOKEN:
        print("Token not available, skipping authenticated test")
        return
    
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(
        f"{API_BASE_URL}/user/me",
        headers=headers
    )
    
    print(f"Response status: {response.status_code}")
    if response.status_code == 200:
        body = response.json()
        print(f"Response body: {body}")
    else:
        print(f"Error response: {response.text}")