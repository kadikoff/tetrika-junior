from collections import defaultdict
import unittest

from bs4 import BeautifulSoup

from task2.tests.mock_data import (
    html_correct_rus,
    html_correct_rus_with_en,
    html_correct_register,
)
from task2.solution_sync import process_animals_data


class TestProcessAnimalsData(unittest.TestCase):
    def setUp(self):
        self.animals_data = defaultdict(int)

    def test_basic_animal_counting(self):
        """Тест базового подсчёта животных"""

        soup = BeautifulSoup(html_correct_rus, "lxml")
        process_animals_data(soup, self.animals_data)

        self.assertEqual(self.animals_data["А"], 2)
        self.assertEqual(self.animals_data["Б"], 1)
        self.assertEqual(len(self.animals_data), 2)

    def test_non_russian_letters_filtering(self):
        """Тест фильтрации не-русских букв"""

        soup = BeautifulSoup(html_correct_rus_with_en, "lxml")
        process_animals_data(soup, self.animals_data)

        self.assertNotIn("A", self.animals_data)
        self.assertNotIn("Z", self.animals_data)
        self.assertEqual(self.animals_data["Ж"], 1)
        self.assertEqual(len(self.animals_data), 1)

    def test_case_insensitivity_register(self):
        """Тест регистронезависимости первой буквы"""

        soup = BeautifulSoup(html_correct_register, "lxml")
        process_animals_data(soup, self.animals_data)

        self.assertEqual(self.animals_data["А"], 2)

    def tearDown(self):
        self.animals_data.clear()
