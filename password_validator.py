import re

# Надежный пароль:
# минимум 8 символов, строчная и заглавная буквы,
# цифра, специальный символ и отсутствие пробелов.
PASSWORD_PATTERN = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-={}\[\]:;,.?])"
    r"[A-Za-z\d!@#$%^&*()_+\-={}\[\]:;,.?]{8,}$"
)

# Используется для поиска возможных паролей в тексте.
CANDIDATE_PATTERN = re.compile(
    r"(?<!\S)[A-Za-z\d!@#$%^&*()_+\-={}\[\]:;,.?]{8,}(?!\S)"
)


def is_strong_password(password: str) -> bool:
    """Проверяет, соответствует ли пароль требованиям надежности."""
    return PASSWORD_PATTERN.fullmatch(password) is not None


def find_strong_passwords(text: str) -> list[str]:
    """Находит в тексте все надежные пароли."""
    candidates = CANDIDATE_PATTERN.findall(text)
    return [item for item in candidates if is_strong_password(item)]
