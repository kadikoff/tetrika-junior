from collections import defaultdict
import os
import csv
import unittest

from task2.tests.mock_data import (
    mock_animals_data,
    csv_file_name,
)
from task2.solution_sync import save_to_csv


class TestSaveToCsv(unittest.TestCase):
    def setUp(self):
        self.animals_data = defaultdict(int, mock_animals_data)

    def test_file_creation(self):
        """Тест создания файла с корректными данными"""

        save_to_csv(self.animals_data, csv_file_name)

        with open(csv_file_name, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)

        self.assertEqual(len(rows), 3)
        self.assertIn(["А", "150"], rows)
        self.assertIn(["Б", "80"], rows)
        self.assertIn(["Я", "5"], rows)

        self.assertEqual(rows[0][0], "А")
        self.assertEqual(rows[1][0], "Б")
        self.assertEqual(rows[2][0], "Я")

    def tearDown(self):
        if os.path.exists(csv_file_name):
            os.remove(csv_file_name)
