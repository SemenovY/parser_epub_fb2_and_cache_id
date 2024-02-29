"""
Импорты.

import sys: Импортирует модуль sys для работы с параметрами командной строки.
import xml.etree.ElementTree as ET: Импортирует модуль xml.etree.ElementTree для работы с XML-структурами.
from typing import Tuple, Union: Импортирует классы Tuple и Union из модуля typing для указания типов данных в функции.
from ebooklib import epub: Импортирует класс epub из библиотеки ebooklib для работы с EPUB-файлами.
"""

import sys
import xml.etree.ElementTree as ET
from typing import Tuple, Union

from ebooklib import epub


def parse_epub(file_path: str) -> Tuple[str, str, str, Union[str, int]]:
    """
    Функция для парсинга метаданных из файла EPUB.

    Читает метаданные из файла EPUB, используя библиотеку ebooklib.
    Обрабатывает возможные ошибки и возвращает кортеж с метаданными.

    Параметры:
    - file_path (str): Путь к файлу EPUB.

    Возвращает кортеж с метаданными (название, автор, издатель, год издания).
    """
    try:
        book = epub.read_epub(file_path)
        title = book.get_metadata("DC", "title")[0][0] if book.get_metadata("DC", "title") else "Unknown Title"
        author = book.get_metadata("DC", "creator")[0][0] if book.get_metadata("DC", "creator") else "Unknown Author"
        publisher = (
            book.get_metadata("DC", "publisher")[0][0] if book.get_metadata("DC", "publisher") else "Unknown Publisher"
        )
        year = int(book.get_metadata("DC", "date")[0][0][:4]) if book.get_metadata("DC", "date") else "Unknown Year"
        return title, author, publisher, year
    except Exception as e:
        print(f"Error reading EPUB file: {e}")
        return "Unknown Title", "Unknown Author", "Unknown Publisher", "Unknown Year"


def parse_fb2(file_path: str) -> Tuple[str, str, str, Union[str, int]]:
    """
    Функция для парсинга метаданных из файла FB2.

    Читает метаданные из файла FB2, используя модуль xml.etree.ElementTree.
    Обрабатывает пространства имен XML и находит соответствующие элементы для извлечения метаданных.
    Обрабатывает возможные ошибки и возвращает кортеж с метаданными.

    Параметры:
    - file_path (str): Путь к файлу FB2.

    Возвращает кортеж с метаданными (название, автор, издатель, год издания).
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        ns = {"fb2": "http://www.gribuser.ru/xml/fictionbook/2.0"}

        title_info = root.find(".//fb2:description/fb2:title-info", namespaces=ns)
        publish_info = root.find(".//fb2:description/fb2:publish-info", namespaces=ns)

        title = (
            title_info.find(".//fb2:book-title", namespaces=ns).text
            if title_info.find(".//fb2:book-title", namespaces=ns) is not None
            else "Unknown Title"
        )
        author = (
            title_info.find(".//fb2:author/fb2:first-name", namespaces=ns).text
            + " "
            + title_info.find(".//fb2:author/fb2:last-name", namespaces=ns).text
            if title_info.find(".//fb2:author", namespaces=ns) is not None
            else "Unknown Author"
        )
        publisher = (
            publish_info.find(".//fb2:publisher", namespaces=ns).text
            if publish_info.find(".//fb2:publisher", namespaces=ns) is not None
            else "Unknown Publisher"
        )
        year = (
            int(publish_info.find(".//fb2:year", namespaces=ns).text)
            if publish_info.find(".//fb2:year", namespaces=ns) is not None
            else "Unknown Year"
        )

        return title, author, publisher, year
    except Exception as e:
        print(f"Error reading FB2 file: {e}")
        return "Unknown Title", "Unknown Author", "Unknown Publisher", "Unknown Year"


def main() -> None:
    """
    Основная часть программы.

    Проверяет количество аргументов командной строки. Если оно не равно 2, выводит сообщение об использовании и завершает программу.
    Получает путь к файлу из командной строки.
    Определяет тип файла (EPUB или FB2) по расширению и вызывает соответствующую функцию для парсинга метаданных.
    Выводит результаты парсинга на экран.
    """
    # Получение аргумента из командной строки:
    if len(sys.argv) != 2:
        print("Usage: python parser.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    # Определение типа файла и вызов соответствующей функции
    if file_path.endswith(".epub"):
        result = parse_epub(file_path)
    elif file_path.endswith(".fb2"):
        result = parse_fb2(file_path)
    else:
        print("Unsupported file format")
        sys.exit(1)

    # Вывод результатов
    print("Title:", result[0])
    print("Author:", result[1])
    print("Publisher:", result[2])
    print("Year:", result[3])


if __name__ == "__main__":
    main()
