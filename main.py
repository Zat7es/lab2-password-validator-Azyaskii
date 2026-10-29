import requests

from file_search import find_passwords_in_file
from password_validator import is_strong_password
from web_search import find_passwords_on_webpage


def print_passwords(passwords: list[str]) -> None:
    """Выводит найденные пароли."""
    if passwords:
        print("Найдены надежные пароли:")
        for password in passwords:
            print(password)
    else:
        print("Надежные пароли не найдены.")


def print_menu() -> None:
    print(
        "\n1 - Проверить пароль\n"
        "2 - Найти надежные пароли в файле\n"
        "3 - Найти надежные пароли на веб-странице\n"
        "0 - Выход"
    )


def main() -> None:
    while True:
        print_menu()
        command = input("Выберите действие: ").strip()

        if command == "1":
            password = input("Введите пароль: ")
            if is_strong_password(password):
                print("Пароль надежный.")
            else:
                print("Пароль не соответствует требованиям.")

        elif command == "2":
            filename = input("Введите путь к текстовому файлу: ").strip()
            try:
                print_passwords(find_passwords_in_file(filename))
            except (FileNotFoundError, OSError, UnicodeError) as error:
                print(f"Ошибка работы с файлом: {error}")

        elif command == "3":
            url = input("Введите URL: ").strip()
            try:
                print_passwords(find_passwords_on_webpage(url))
            except requests.RequestException as error:
                print(f"Ошибка загрузки страницы: {error}")

        elif command == "0":
            print("Работа программы завершена.")
            break

        else:
            print("Неизвестная команда.")


if __name__ == "__main__":
    main()
