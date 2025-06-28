# Yavshok API Tests

Automated tests for [Yavshok REST API](https://api.yavshok.ru/swagger)

## Установка

1. Для клонирования репозитория:
   ```bash
   git clone https://github.com/your-username/yavshok_api_tests.git
   cd yavshok_api_tests

2. Для запуска тестов:
    ```bash
    pytest src/tests/ -v

3. Для запуска тестов с выводом дополнительной информации:
   ```bash
   pytest src/tests/test_direct_requests.py -v -s