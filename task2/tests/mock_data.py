# Первая страница из категории "Животные по алфавиту"
start_url = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"

# Вторая страница из категории "Животные по алфавиту"
second_url = (
    "/w/index.php?title=%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:"
    "%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB"
    "%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83&pagefrom=%D0%90%D0%B7%D0%B8%D0%B0%D1%"
    "82%D1%81%D0%BA%D0%B8%D0%B5+%D1%82%D0%BE%D0%BA%D0%B8#mw-pages"
)

# Последняя страница из категории "Животные по алфавиту"
end_url = (
    "https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту&"
    "pagefrom=Zosterops+lateralis#mw-pages"
)
invalid_url = "https://ru.wikipedia.org/Категория:Животные_по_алфавиту"

html_correct_rus = """
    <div class="mw-category-group">
        <h3>А</h3>
        <ul>
            <li>Аист</li>
            <li>Акула</li>
        </ul>
        <h3>Б</h3>
        <ul>
            <li>Барсук</li>
        </ul>
    </div>
"""
html_correct_rus_with_en = """
    <div class="mw-category-group">
        <h3>A</h3>
        <ul>
            <li>Antelope</li>
        </ul>
        <h3>Ж</h3>
        <ul>
            <li>Жираф</li>
        </ul>
        <h3>Z</h3>
        <ul>
            <li>Zebra</li>
        </ul>
    </div>
"""
html_correct_register = """
    <div class="mw-category-group">
        <h3>А</h3>
        <ul>
            <li>аист</li>
            <li>Акула</li>
        </ul>
    </div>
"""

mock_animals_data = {
    'А': 150,
    'Б': 80,
    'Я': 5
}
csv_file_name = "test_animals.csv"
