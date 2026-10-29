from pathlib import Path

from password_validator import find_strong_passwords


def find_passwords_in_file(filename: str) -> list[str]:
    """Читает текстовый файл и ищет в нем надежные пароли."""
    path = Path(filename)

    if not path.exists():
        raise FileNotFoundError(f"Файл '{filename}' не найден.")

    text = path.read_text(encoding="utf-8")
    return find_strong_passwords(text)
