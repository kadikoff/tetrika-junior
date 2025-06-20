import unittest

from task3.solution_2 import appearance
from task3.tests.mock_data import tests


class TestAppearance(unittest.TestCase):
    def test_success(self):
        """Проверяет, что данные с расчётов сходятся с заданным ответом"""

        for i, test in enumerate(tests):
            with self.subTest(**test):
                test_answer = appearance(test['intervals'])
                assert test_answer == test[
                    'answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
