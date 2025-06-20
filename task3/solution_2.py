def merge_intervals(intervals: list[int]) -> list[tuple[int, int]]:
    """
    Объединяет пересекающиеся интервалы присутствия в единый список кортежей.
    Возвращает временные интервалы без пересечений в виде пар (начало, конец).

    Алгоритм:
    1. Разбивает входные данные на пары (вход, выход)
    2. Сортирует интервалы по времени начала
    3. Объединяет пересекающиеся интервалы
    4. Возвращает список объединённых интервалов

    Пример:
        Вход:
            intervals = [10, 20, 15, 25]
        Выход:
            merged = [(10, 25)]

    :param intervals: временные интервалы присутствия ученика/преподавателя
    :return: список кортежей объединённых интервалов
    """
    if not intervals:
        return []

    pairs = list(zip(intervals[::2], intervals[1::2]))
    pairs.sort(key=lambda x: x[0])

    merged = []
    current_start, current_end = pairs[0]

    for start, end in pairs[1:]:
        if start <= current_end:
            current_end = max(current_end, end)
        else:
            merged.append((current_start, current_end))
            current_start, current_end = start, end

    merged.append((current_start, current_end))
    return merged


def find_intersections(
        pupil: list[tuple[int, int]],
        tutor: list[tuple[int, int]]
) -> list[tuple[int, int]]:
    """
    Находит временные интервалы одновременного присутствия ученика и учителя.
    Возвращает список пересечений интервалов в виде пар (начало, конец).

    Алгоритм:
    1. Использует метод двух указателей для эффективного сравнения интервалов
    2. Для каждой пары интервалов вычисляет:
       - Позднее начало (максимум из начал)
       - Ранний конец (минимум из концов)
    3. Если интервалы пересекаются (позднее начало < ранний конец),
       добавляет пересечение в результат

    Пример:
        Вход:
            pupil = [(10, 20), (30, 40)]
            tutor = [(15, 25), (35, 45)]
        Выход:
            intersections = [(15, 20), (35, 40)]

    :param pupil: временные интервалы присутствия ученика
    :param tutor: временные интервалы присутствия учителя
    :return: список пересечений интервалов
    """
    if not pupil or not tutor:
        return []

    intersections = []
    i = j = 0

    while i < len(pupil) and j < len(tutor):
        start_p, end_p = pupil[i]
        start_t, end_t = tutor[j]

        start_max = max(start_p, start_t)
        end_min = min(end_p, end_t)

        if start_max < end_min:
            intersections.append((start_max, end_min))

        if end_p < end_t:
            i += 1
        else:
            j += 1

    return intersections


def calculate_time(
        intersections: list[tuple[int, int]], lesson: list[int]
) -> int:
    """
    Вычисляет общее время одновременного присутствия ученика и учителя на уроке.

    Алгоритм:
    1. Для каждого интервала пересечения:
       - Обрезает начало по началу урока (если интервал начинается раньше)
       - Обрезает конец по концу урока (если интервал заканчивается позже)
    2. Суммирует длительности всех валидных интервалов

    Пример:
        Вход:
            intersections = [(15, 20), (35, 40)]
            lesson = [10, 50]
        Выход - решение:
            (20-15) + (40-35) = 5 + 5 = 10

    :param intersections: список пересечений интервалов
    :param lesson: границы урока
    :return: суммарное время присутствия на уроке
    """
    total_time = 0
    lesson_start, lesson_end = lesson

    for start, end in intersections:
        start_clipped = max(start, lesson_start)
        end_clipped = min(end, lesson_end)

        if start_clipped < end_clipped:
            total_time += end_clipped - start_clipped

    return total_time


def appearance(intervals: dict[str, list[int]]) -> int:
    """
    Вычисляет общее время одновременного присутствия ученика и учителя на уроке.

    Алгоритм работы:
        1. Объединяет интервалы присутствия ученика и учителя (устраняет перекрытия)
        2. Находит пересечения обработанных интервалов ученика и учителя
        3. Вычисляет время совместного присутствия

    Особенности:
        - Интервалы могут быть не отсортированы и перекрываться
        - Границы урока имеют приоритет
        - Сложность: O(n log n) из-за сортировки и объединения интервалов
    """
    lesson = intervals["lesson"]
    pupil = intervals["pupil"]
    tutor = intervals["tutor"]

    pupil_merged = merge_intervals(pupil)
    tutor_merged = merge_intervals(tutor)

    intersections = find_intersections(pupil_merged, tutor_merged)
    if not intersections:
        return 0

    total_time = calculate_time(intersections, lesson)

    return total_time


if __name__ == "__main__":
    tests = [
        {
            'intervals':
                {
                    'lesson': [1594663200, 1594666800],
                    'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
                    'tutor': [1594663290, 1594663430, 1594663443, 1594666473]
                },
            'answer': 3117
        },
        {
            'intervals':
                {
                    'lesson': [1594702800, 1594706400],
                    'pupil': [
                        1594702789, 1594704500, 1594702807, 1594704542,
                        1594704512, 1594704513, 1594704564, 1594705150,
                        1594704581, 1594704582, 1594704734, 1594705009,
                        1594705095, 1594705096, 1594705106, 1594706480,
                        1594705158, 1594705773, 1594705849, 1594706480,
                        1594706500, 1594706875, 1594706502, 1594706503,
                        1594706524, 1594706524, 1594706579, 1594706641
                    ],
                    'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
            'answer': 3577
        },
        {
            'intervals':
                {
                    'lesson': [1594692000, 1594695600],
                    'pupil': [1594692033, 1594696347],
                    'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
            'answer': 3565
        },
    ]

    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
