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
    books = book_gen()
    out = [getbook(books) for _ in range(100)]
    with open('out.json', 'w') as fd:
        fd.write(dumps(out, indent=2, ensure_ascii=False))
    return


def titles_gen() -> str:
    """
    Генератор. Возвращает случайно выбранное название из списка в файле.
    :return: str
    """
    index = []
    with open('fakebooks.txt', 'rt') as fd:
        start = -1
        while start != fd.tell():
            start = fd.tell()
            line =  fd.readline()
            line = line.rstrip()
            if not line:
                continue
            index.append([start, len(line)])
    while True:
        i = choice(index)
        with open('fakebooks.txt') as fd:
            fd.seek(i[0])
            name = fd.read(i[1])
        yield name
#    with open('fakebooks.txt') as fd:
#        booknames = fd.readlines()
#    while True:
#        yield choice(booknames).rstrip()


def year() -> int:
    """
    Возвращает случайный год; диапазон 1900-2021.
    :return: int
    """
    return randint(1900, 2021)


def pages() -> int:
    """
    Возвращает случайное число страниц; диапазон 10 - 1000.
    :return: int
    """
    return randint(10, 1000)


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
    return round(uniform(0, 5), 2)


def price() -> float:
    """
    Возвращает случайную цену; диапазон 100.00-1000.00
    :return: float
    """
    return round(uniform(100, 1000), 2)


def authors() -> list:
    """
    Возвращает от одного до трех случайно сгенерированных авторов
    :return: list
    """
    return [FAKE.name() for _ in range(randint(1, 3))]


def lengthcheck(maxlen):
    """
    Фабрика декораторов для проверки длины названия книг.
    :param maxlen: Максимальная длина названия.
    :return: Декоратор для проверки.
    """
    def decorator(fn):
        def wrapper(*args):
            book = fn(*args)
            if len(book['fields']['title']) > maxlen:
                raise ValueError(f"Слишком длинное название книги: '{book['fields']['title']}'.")
            return book
        return wrapper
    return decorator


@lengthcheck(32)
def getbook(books):
    """
    Враппер для возможности использовать декоратор.
    :param books: Итератор
    :return: dict
    """
    return next(books)


def book_gen(counter: int = 1) -> Iterator[dict]:
    """
    Возвращает итератор для случайной генерации книг.
    :param counter: Стартовое значение для индекса книги, по-умолчанию 1
    :return: dict
    """
    title = titles_gen()
    while True:
        yield {
            'model': MODEL,
            'pk': counter,
            'fields': {
                "title": next(title),
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
