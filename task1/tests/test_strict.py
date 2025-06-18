import unittest

from task1.solution import strict
from task1.tests.mock_data import correct_test_cases, incorrect_test_cases


class TestStrict(unittest.TestCase):

    @staticmethod
    @strict
    def _test_func(a, b):
        return a + b

    def test_correct_types_no_errors(self):
        """Проверяет, что функция с правильными типами работает без ошибок"""

        for test_case in correct_test_cases:
            annotations = test_case["annotations"]
            self._test_func.__annotations__ = annotations

            with self.subTest(**test_case):
                result = self._test_func(*test_case["args"], **test_case["kwargs"])
                self.assertIsInstance(result, annotations.get("return", type(result)))

    def test_incorrect_types_errors(self):
        """Проверяет, что функция с не правильными типами обрабатывает ошибку"""

        for test_case in incorrect_test_cases:
            annotations = test_case["annotations"]
            self._test_func.__annotations__ = annotations

            with self.subTest(**test_case):
                with self.assertRaises(TypeError):
                    self._test_func(*test_case["args"], **test_case["kwargs"])
