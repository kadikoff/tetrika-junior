from collections import defaultdict
import csv
from datetime import datetime
from typing import Optional

import requests
from bs4 import BeautifulSoup


def process_page(
        current_url: str,
        animals_count_data: defaultdict[str, int],
) -> Optional[str]:
    """Обработка полученной страницы

    - извлечение, обработка и подсчёт кол-ва животных с занесением информации
    во временное хранилище - словарь animals_count_data;
    - получение ссылки на следующую страницу;
    """
    try:
        response = requests.get(current_url)
    except Exception as exc:
        print(f"Ошибка при запросе {current_url}: {exc}")
        return None

    soup = BeautifulSoup(response.text, "lxml")
    common_div = soup.find("div", id="mw-pages")
    if not common_div:
        return None

    # Обработка животных, название которых на русском языке
    process_animals_data(common_div, animals_count_data)

    # Получение ссылки на следующую страницу
    next_page = soup.find("a", string="Следующая страница")
    return next_page["href"] if next_page else None


def process_animals_data(
        common_div: BeautifulSoup, animals_count_data: defaultdict[str, int]
) -> None:
    """Извлечение, обработка и подсчёт кол-ва животных с занесением информации
    во временное хранилище - словарь animals_count_data;
    """
    animals_div = (
        common_div
        .find("div", class_="mw-category-group")
        .find_all("li")
    )
    for animal_name in animals_div:
        animal_first_letter = animal_name.text[0].upper()

        if "А" <= animal_first_letter <= "Я":
            animals_count_data[animal_first_letter] += 1


def crawl_wikipedia(start_url: str) -> defaultdict[str, int]:
    """Синхронно собирает количество животных по алфавиту.

    Обходит страницы категории "Животные по алфавиту" на русской Википедии,
    начиная с указанной стартовой страницы, и подсчитывает количество животных
    для каждой буквы русского алфавита.
    """
    animals_count_data = defaultdict(int)
    base_url = "https://ru.wikipedia.org"
    current_url = start_url

    while True:
        next_page_url: Optional[str] = process_page(
            current_url, animals_count_data
        )
        if not next_page_url:
            break
        current_url = base_url + next_page_url

    return animals_count_data


def save_to_csv(
        data: defaultdict[str, int], filename: str = "animals_1.csv"
) -> None:
    """Сохраняет данные о количестве животных в .csv-файл
    в формате 'Буква, количество' - 'А, 1600'.
    """
    sorted_data = sorted(data.items(), key=lambda x: x[0])

    with open(filename, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        for letter, count in sorted_data:
            writer.writerow([letter, count])


def main():
    start_url = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"

    # Подсчёт кол-ва животных по алфавиту
    animals_data = crawl_wikipedia(start_url)

    # Сохранение данных в .csv-файл
    save_to_csv(data=animals_data)


if __name__ == "__main__":
    start = datetime.now()
    main()
    end = datetime.now() - start

    print("Время выполнения программы: ", end)
