#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Есть массив объектов, которые имеют поля `id` и `parent`, через которые их можно связать
в дерево и некоторые произвольные поля.

Нужно написать класс, который принимает в конструктор массив этих объектов и реализует 4 метода:
- getAll()    -- Должен возвращать изначальный массив элементов.
- getItem(id) -- Принимает `id` элемента и возвращает сам объект элемента;
- getChildren(id)   -- Принимает `id` элемента и возвращает массив элементов, являющихся дочерними для того элемента,
                       чей `id` получен в аргументе. Если у элемента нет дочерних, то должен возвращаться пустой массив;
- getAllParents(id) -- Принимает `id` элемента и возвращает массив из цепочки родительских элементов,
                       начиная от самого элемента, чей `id` был передан в аргументе и до корневого элемента,
                       т.е. должен получиться путь элемента наверх дерева через цепочку родителей к корню дерева.
                       Порядок элементов важен!

Требования: максимальное быстродействие, следовательно, минимальное количество обходов массива при операциях,
в идеале, прямой доступ к элементам без поиска их в массиве.

Примеры использования:
- ts.getAll()         -> [{'id': 1, 'parent': None},
                          {'id': 2, 'parent': 1, 'type': 'test'},
                          {'id': 3, 'parent': 1, 'type': 'test'},
                          {'id': 4, 'parent': 2, 'type': 'test'},
                          {'id': 5, 'parent': 2, 'type': 'test'},
                          {'id': 6, 'parent': 2, 'type': 'test'},
                          {'id': 7, 'parent': 4, 'type': None},
                          {'id': 8, 'parent': 4, 'type': None}]
- ts.getItem(7)       -> {'id': 7, 'parent': 4, 'type': None}
- ts.getChildren(4)   -> [{'id': 7, 'parent': 4, 'type': None},
                          {'id': 8, 'parent': 4, 'type': None}]
- ts.getChildren(5)   -> []
- ts.getAllParents(7) -> [{'id': 4, 'parent': 2, 'type': 'test'},
                          {'id': 2, 'parent': 1, 'type': 'test'},
                          {'id': 1, 'parent': None}]
"""

import itertools as I
import operator  as O


class TreeStore:
    def __init__(self, items):
        self.__items = {item['id']: item for item in items}
        self.__chlds = {pid: [item['id'] for item in items]
            for pid, items in I.groupby(self.__items.values(), O.itemgetter('parent'))}

    def getAll(self):
        return list(self.__items.values())

    def getItem(self, ident, default=None):
        return self.__items.get(ident, default)

    def getChildren(self, ident):
        return list(map(self.getItem, self.__chlds.get(ident, [])))

    def getAllParents(self, ident):
        parent_id = self.getItem(ident, {}).get('parent')
        if parent_id is not None:
            parent = self.getItem(parent_id)
            return [parent] + self.getAllParents(parent['id'])
        return []


def main():
    items = [
        {'id': 1, 'parent': None},
        {'id': 2, 'parent': 1, 'type': 'test'},
        {'id': 3, 'parent': 1, 'type': 'test'},
        {'id': 4, 'parent': 2, 'type': 'test'},
        {'id': 5, 'parent': 2, 'type': 'test'},
        {'id': 6, 'parent': 2, 'type': 'test'},
        {'id': 7, 'parent': 4, 'type': None},
        {'id': 8, 'parent': 4, 'type': None}
    ]

    ts = TreeStore(items)

    import pprint
    pprint.pprint(ts.getAll())

    assert ts.getItem(7) == {'id': 7, 'parent': 4, 'type': None}

    assert ts.getChildren(4) == [
        {'id': 7, 'parent': 4, 'type': None},
        {'id': 8, 'parent': 4, 'type': None}]

    assert ts.getChildren(5) == []

    assert ts.getAllParents(7) == [
        {'id': 4, 'parent': 2, 'type': 'test'},
        {'id': 2, 'parent': 1, 'type': 'test'},
        {'id': 1, 'parent': None}]

    print('All tests successful')


if __name__ == '__main__':
    main()
