import requests

from password_validator import find_strong_passwords


def find_passwords_on_webpage(url: str) -> list[str]:
    """Загружает веб-страницу по URL и ищет надежные пароли."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return find_strong_passwords(response.text)
