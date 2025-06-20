def merge_intervals(pupil: list[int], tutor: list[int]) -> list[int]:
    """
    Объединяет пересекающиеся интервалы присутствия ученика и учителя в единый список.
    Возвращает временные интервалы, где хотя бы один присутствовал, без пересечений.

    Алгоритм:
    1. Разбивает входные данные на пары (вход, выход)
    2. Сортирует интервалы по времени начала
    3. Объединяет пересекающиеся интервалы для каждого участника
    4. Объединяет результаты ученика и учителя в один список

    Пример:
        Вход:
            pupil = [10, 20, 15, 25]
            tutor = [5, 12, 30, 35]
        Выход:
            merged_intervals = [5, 25, 30, 35]

    :param pupil: временные интервалы присутствия ученика
    :param tutor: временные интервалы присутствия учителя
    :return: список интервалов присутствия ученика и учителя
    """

    lesson_start, lesson_end = lesson
    merged_intervals = []

    for data in [pupil, tutor]:
        pairs = list(zip(data[::2], data[1::2]))

        pairs.sort(key=lambda x: x[0])

        merged = []
        if not pairs:
            return []

        current_start, current_end = pairs[0]

        for start, end in pairs[1:]:
            # Если кто-то ушёл до начала урока
            # или присоединился после его окончания - не считаем
            if end <= lesson_start or start >= lesson_end:
                continue

            if start <= current_end:
                current_end = max(current_end, end)
            else:
                merged.append((current_start, current_end))
                current_start, current_end = start, end

        merged.append((current_start, current_end))

        for start, end in merged:
            merged_intervals.append(start)
            merged_intervals.append(end)

    return merged_intervals


def get_border_time(
        merged_intervals: list[int], lesson: list[int],
) -> list[int]:
    """
    Определяет актуальные границы присутствия ученика/учителя в рамках урока.
    Возвращает интервал [начало, конец], не выходит за границы начала и конца урока.

    Пример:
        Вход:
            merged_intervals = [5, 25, 30, 35]
            lesson = [6, 37]
        Выход:
            l_r_border_time = [6, 35]

    :param merged_intervals: список интервалов присутствия ученика и учителя
    :param lesson: начало и конец урока
    :return: временные границы
    """

    l_border_time = max(lesson[0], merged_intervals[0])
    r_border_time = min(lesson[-1], merged_intervals[-1])

    return [l_border_time, r_border_time]


def binary_search_pos_borders(
        merged_intervals: list[int], l_r_border_time: list[int]
) -> list[int]:
    """
    Находит индексы временных границ в отсортированном списке интервалов.
    Использует бинарный поиск для эффективного определения позиций.

    Пример:
        Вход:
            merged_intervals = [5, 25, 30, 35]
            l_r_border_time = [6, 35]
        Выход:
            l_r_border_idxs = [1, 3]

    :param merged_intervals: список интервалов присутствия ученика и учителя
    :param l_r_border_time: временные границы которые нужно найти в списке
    :return: позиции (индексы) временных границ
    """

    l_r_border_idxs = []

    for border in [l_r_border_time[0], l_r_border_time[-1]]:
        left = 0
        right = len(merged_intervals) - 1

        while left < right:
            middle = (left + right) // 2
            if merged_intervals[middle] < border:
                left = middle + 1
            else:
                right = middle

        border_idx = left
        l_r_border_idxs.append(border_idx)

    return l_r_border_idxs


def cut_merged_intervals(
        merged_intervals: list[int],
        l_r_border_time: list[int],
        l_r_border_idxs: list[int],
) -> list[int]:
    """
    Обрезает список интервалов по заданным временным границам, возвращая только интервалы,
    которые полностью попадают в указанные границы.

    Пример:
        Вход:
            merged_intervals = [5, 6, 25, 30, 35]
            l_r_border_time = [6, 35]
            l_r_border_idxs = [1, 3]
        Выход:
            cut_intervals = [25, 30]

    :param merged_intervals: список интервалов присутствия ученика и учителя
    :param l_r_border_time: временные границы
    :param l_r_border_idxs: индексы временных границы в merged_intervals
    :return: позиции (индексы) временных границ
    """

    l_border_time, r_border_time = l_r_border_time
    l_border_idx, r_border_idx = l_r_border_idxs

    if merged_intervals[0] == l_border_time and merged_intervals[-1] == r_border_time:
        return merged_intervals

    return merged_intervals[l_border_idx: r_border_idx]


def calculate_time(
        cut_intervals: list[int], l_r_border_time: list[int]
) -> int:
    """
    Вычисляет общее время одновременного присутствия ученика и учителя на уроке.

    Алгоритм:
    1. Рассчитывает полное время урока между границами
    2. Вычитает из него все периоды, когда хотя бы один отсутствовал
    3. Возвращает суммарное время совместного присутствия

    Пример:
        Вход:
            cut_intervals = [25, 30]
            l_r_border_time = [6, 35]

        Решение:
            1. Полное время урока: 35 - 6 = 29
            2. Время отсутствия: 30 - 25 = 5
            3. Совместное время: 29 - 5 = 24

        Выход:
            result = 24

    :param cut_intervals: список интервалов присутствия ученика и учителя
    в новых границах
    :param l_r_border_time: временные границы
    :return: суммарное время присутствия на уроке
    """

    l_border_time, r_border_time = l_r_border_time
    common_time = r_border_time - l_border_time
    common_diff = 0

    for idx, time in enumerate(cut_intervals):
        if idx % 2 != 0:
            common_diff += time - cut_intervals[idx - 1]

    return common_time - common_diff


def appearance(intervals: dict[str, list[int]]) -> int:
    """
    Вычисляет общее время одновременного присутствия ученика и учителя на уроке.

    Алгоритм работы:
        1. Объединяет интервалы присутствия ученика и учителя (устраняет перекрытия)
        2. Определяет границы анализа (пересечение с временем урока)
        3. Находит позиции этих границ в объединённых интервалах
        4. Обрезает интервалы по границам урока
        5. Вычисляет время совместного присутствия

    Особенности:
        - Интервалы могут быть не отсортированы и перекрываться
        - Границы урока имеют приоритет
        - Сложность: O(n log n) из-за сортировки и объединения интервалов
    """
    lesson = intervals["lesson"]
    pupil = intervals["pupil"]
    tutor = intervals["tutor"]

    merged_intervals = merge_intervals(pupil, tutor, lesson)
    if not merged_intervals:
        return 0

    merged_intervals.sort()

    l_r_border_time = get_border_time(merged_intervals, lesson)

    l_r_border_idxs = binary_search_pos_borders(merged_intervals, l_r_border_time)

    cut_intervals = cut_merged_intervals(merged_intervals, l_r_border_time, l_r_border_idxs)

    result_timestamp = calculate_time(cut_intervals, l_r_border_time)

    return result_timestamp


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
                    1594702789, 1594704500,
                    1594702807, 1594704542,
                    1594704512, 1594704513,
                    1594704564, 1594705150,
                    1594704581, 1594704582,
                    1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480,
                    1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503,
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

if __name__ == "__main__":
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
