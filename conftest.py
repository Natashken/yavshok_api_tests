import pytest
from dotenv import load_dotenv
import os
from src.client.api_client import ApiClient
from src.client.endpoints.auth import AuthEndpoint
from src.client.endpoints.user import UserEndpoint

# Загружаем переменные окружения один раз для всех тестов
load_dotenv()

@pytest.fixture(scope="session")
def api_base_url():
    """Фикстура для базового URL API"""
    url = os.getenv('API_BASE_URL')
    if not url:
        raise RuntimeError("API_BASE_URL is not set in environment variables")
    return url

@pytest.fixture(scope="session")
def api_username():
    """Фикстура для имени пользователя"""
    username = os.getenv('API_USERNAME')
    if not username:
        raise RuntimeError("API_USERNAME is not set in environment variables")
    return username

@pytest.fixture(scope="session")
def api_password():
    """Фикстура для пароля пользователя"""
    password = os.getenv('API_PASSWORD')
    if not password:
        raise RuntimeError("API_PASSWORD is not set in environment variables")
    return password

@pytest.fixture
def client(api_base_url):
    """Фикстура для создания клиента"""
    return ApiClient(api_base_url)

@pytest.fixture
def auth_endpoint(client):
    """Фикстура для создания эндпоинта авторизации"""
    return AuthEndpoint(client)

@pytest.fixture
def user_endpoint(client):
    """Фикстура для создания эндпоинта пользователя"""
    return UserEndpoint(client)

@pytest.fixture
def shock_endpoint(client):
    """Фикстура для создания эндпоинта shock"""
    return client
