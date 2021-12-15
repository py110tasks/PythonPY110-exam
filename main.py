#!/usr/bin/env python3

from random import random, randint, uniform
from random import choice
from json import dumps
from typing import Iterator

from faker import Faker

from conf import MODEL

FAKE = Faker()


def main() -> None:
    """
    Генерирует список из 100 случайно сгенерированных книг и записывает в файл в формате JSON.
    """
    books = iter(book())  # todo always iterator
    out = [next(books) for _ in range(100)]
    with open('out.json', 'w') as fd:
        fd.write(dumps(out, indent=2, ensure_ascii=False))
    return


def title() -> str:
    """
    Генератор. Возвращает случайно выбранное название из списка в файле.
    :return: str
    """
    with open('fakebooks.txt') as fd:
        booknames = fd.readlines()
    while True:
        yield choice(booknames).rstrip('\n').rstrip('\r')  # fixme rstrip()

def year() -> int:
    """
    Возвращает случайный год; диапазон 1900-2021.
    :return: int
    """
    return int(1900 + random() * 121)  # todo randint


def pages() -> int:
    """
    Возвращает случайное число страниц; диапазон 10 - 1010.
    :return: int
    """
    return int(10 + random() * 1000)


def isbn() -> str:
    """
    Возвращает случайный ISBN.
    :return: str
    """
    return FAKE.isbn13()


def rating() -> float:
    """
    Возвращает случайный рейтинг; диапазон 0-5
    :return: float
    """
    return round(random() * 5, 2)  # uniform


def price() -> float:
    """
    Возвращает случайную цену; диапазон 100.00-1000.00
    :return: float
    """
    return round(100 + random() * 1000, 2)


def authors() -> list[str]:
    """
    Возвращает от одного до трех случайно сгенерированных авторов
    :return: list
    """
    return [FAKE.name() for _ in range(int(random() * 2.9) + 1)]


def book(counter: int = 1) -> Iterator[dict]:
    """
    Возвращает случайно сгенерированую книгу.
    :param counter: Стартовое значение для индекса книги, по-умолчанию 1
    :return: dict
    """
    while True:
        yield {
            'model': MODEL,
            'pk': counter,
            'fields': {
                "title": next(title()),  # fixme каждый раз инициализация?
                "year": year(),
                "pages": pages(),
                "isbn13": isbn(),
                "rating": rating(),
                "price": price(),
                "author": authors()
            }
        }
        counter += 1


if __name__ == '__main__':
    main()
