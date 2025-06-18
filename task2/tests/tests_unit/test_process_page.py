from collections import defaultdict
import unittest

from task2.tests.mock_data import (
    start_url,
    second_url,
    end_url,
    invalid_url,
)
from task2.solution_sync import process_page


class TestProcessPage(unittest.TestCase):

    def setUp(self):
        self.animals_data = defaultdict(int)

    def test_first_page_processing(self):
        """Тест обработки первой страницы со ссылкой на следующую"""

        next_page_url = process_page(start_url, self.animals_data)
        self.assertEqual(second_url, next_page_url)

    def test_last_page_processing(self):
        """Тест обработки последней страницы без ссылки на следующую"""

        next_page_url = process_page(end_url, self.animals_data)
        self.assertIsNone(next_page_url)

    def test_page_processing_invalid_url(self):
        """Тест обработки страницы с невалидной ссылкой"""

        next_page_url = process_page(invalid_url, self.animals_data)
        self.assertIsNone(next_page_url)

    def tearDown(self):
        self.animals_data.clear()
