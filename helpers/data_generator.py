import random
import string


def generate_random_email() -> str:
    return f"test_{random.randint(100000, 999999)}@yandex.ru"


def generate_random_password() -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))