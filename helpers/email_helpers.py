import uuid


def generate_email() -> str:
    """
    Генерирует уникальный email на каждый вызов, чтобы тесты регистрации
    не конфликтовали с уже существующими в системе пользователями.
    """
    unique_part = uuid.uuid4().hex[:10]
    return f"user_{unique_part}@example.com"
