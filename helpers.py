import time

def generate_random_user_credentials():
    # Вспомогательный метод генерирует уникальные данные для регистрации нового пользователя
    unique_email = f"user_{int(time.time())}@test.ru"
    password = "TestPassword123!"
    return {
        "email": unique_email,
        "password": password
    }
