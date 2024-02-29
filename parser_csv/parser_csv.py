import csv
import os
from collections import Counter
from typing import List

OCCURRENCES_IDS = 3
FILE_NAME = os.path.join(os.path.dirname(__file__), "table.csv")


def read_data_from_csv_file(file: str) -> List[str]:
    """
    csv.DictReader.

    В каждой итерации, csv.DictReader возвращает строку файла CSV в виде словаря,
    где ключи - это заголовки столбцов, а значения - соответствующие значения в текущей строке.
    В отличие от csv.reader, где нужно обращаться к данным по индексу,
    DictReader позволяет обращаться к данным по ключу, что делает код более читаемым и уменьшает зависимость от порядка столбцов.

    :param FILE_NAME: Путь к CSV-файлу.
    :return: Список идентификаторов из файла.
    """
    ids = []
    with open(file, "r", newline="", encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            ids.append(row["id"])
    return ids


def find_ids(ids: List[str]) -> List[str]:
    """
    Возвращает уникальные идентификаторы, которые встречаются ровно 3 раза в списке.

    :param ids: Список идентификаторов.
    :return: Список уникальных идентификаторов с тремя повторениями.
    """
    ids_count = Counter(ids)
    return [id for id, count in ids_count.items() if count == OCCURRENCES_IDS]


def count_occurrences_frequency(ids: List[str]) -> Counter:
    """
    Возвращает частоту повторений уникальных идентификаторов в списке.

    :param ids: Список идентификаторов.
    :return: Счетчик, представляющий частоту повторений.
    """
    return Counter(Counter(ids).values())


def get_word_form(number: int, one_form: str, two_four_form: str, other_form: str) -> str:
    """
    Определяет правильную форму слова в зависимости от числа.

    :param number: Число для определения формы слова.
    :param one_form: Форма слова для числа 1.
    :param two_four_form: Форма слова для чисел 2, 3, 4.
    :param other_form: Форма слова для остальных чисел.
    :return: Правильная форма слова в зависимости от числа.
    """
    if number % 10 == 1 and number % 100 != 11:
        return one_form
    elif 2 <= number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
        return two_four_form
    else:
        return other_form


if __name__ == "__main__":

    # Задача 1: Вывести id, которые встречаются только 3 раза
    ids = read_data_from_csv_file(FILE_NAME)
    ids_with_three_occurrences = find_ids(ids)
    print("Задача 1:")
    print(ids_with_three_occurrences)

    # Задача 2: Вывести частоту повторений
    occurrences_frequency = count_occurrences_frequency(ids)
    print("\nЗадача 2:")
    for occurrences, count in occurrences_frequency.items():
        word_form = get_word_form(occurrences, "раз", "раза", "раз")
        print(f"{count} уникальных id встречались {occurrences} {word_form}")
