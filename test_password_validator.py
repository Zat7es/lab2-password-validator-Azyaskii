import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import requests

from file_search import find_passwords_in_file
from password_validator import find_strong_passwords, is_strong_password
from web_search import find_passwords_on_webpage


class PasswordValidatorTests(unittest.TestCase):
    """Тесты проверки одного пароля."""

    def test_valid_passwords(self) -> None:
        passwords = [
            "Qwerty123!",
            "Strong_7A",
            "Abcdef1?",
            "MyPass2026#",
        ]
        for password in passwords:
            with self.subTest(password=password):
                self.assertTrue(is_strong_password(password))

    def test_too_short_password(self) -> None:
        self.assertFalse(is_strong_password("Aa1!abc"))

    def test_without_uppercase_letter(self) -> None:
        self.assertFalse(is_strong_password("qwerty123!"))

    def test_without_lowercase_letter(self) -> None:
        self.assertFalse(is_strong_password("QWERTY123!"))

    def test_without_digit(self) -> None:
        self.assertFalse(is_strong_password("Qwerty!!!"))

    def test_without_special_character(self) -> None:
        self.assertFalse(is_strong_password("Qwerty123"))

    def test_password_with_space(self) -> None:
        self.assertFalse(is_strong_password("Qwerty 123!"))

    def test_empty_password(self) -> None:
        self.assertFalse(is_strong_password(""))


class PasswordSearchTests(unittest.TestCase):
    """Тесты поиска надежных паролей в тексте."""

    def test_find_passwords_in_text(self) -> None:
        text = "Qwerty123! weakpass Strong_7A PASSWORD1!"
        self.assertEqual(
            find_strong_passwords(text),
            ["Qwerty123!", "Strong_7A"],
        )

    def test_text_without_valid_passwords(self) -> None:
        self.assertEqual(find_strong_passwords("qwerty password 12345678"), [])


class FileSearchTests(unittest.TestCase):
    """Тесты поиска в локальном файле."""

    def test_find_passwords_in_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "passwords.txt"
            path.write_text(
                "Qwerty123!\nweakpass\nStrong_7A",
                encoding="utf-8",
            )
            self.assertEqual(
                find_passwords_in_file(str(path)),
                ["Qwerty123!", "Strong_7A"],
            )

    def test_missing_file(self) -> None:
        with self.assertRaises(FileNotFoundError):
            find_passwords_in_file("missing_file_12345.txt")


class WebSearchTests(unittest.TestCase):
    """Тесты поиска на веб-странице без реального обращения в интернет."""

    @patch("web_search.requests.get")
    def test_find_passwords_on_webpage(self, mock_get: Mock) -> None:
        response = Mock()
        response.text = "Qwerty123! weakpass Strong_7A"
        response.raise_for_status.return_value = None
        mock_get.return_value = response

        self.assertEqual(
            find_passwords_on_webpage("https://example.com"),
            ["Qwerty123!", "Strong_7A"],
        )
        mock_get.assert_called_once_with("https://example.com", timeout=10)

    @patch("web_search.requests.get")
    def test_web_request_error(self, mock_get: Mock) -> None:
        mock_get.side_effect = requests.RequestException("Network error")

        with self.assertRaises(requests.RequestException):
            find_passwords_on_webpage("https://example.com")


if __name__ == "__main__":
    unittest.main()
