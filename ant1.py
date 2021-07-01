#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
На бесконечной координатной сетке находится муравей. Муравей может перемещаться на 1 клетку вверх
(x,y+1), вниз (x,y-1), влево (x-1,y), вправо (x+1,y), по одной клетке за шаг.

Клетки, в которых сумма цифр в координате X плюс сумма цифр в координате Y больше чем 25 недоступны муравью.
Например, клетка с координатами (59, 79) недоступна, т.к. 5+9+7+9=30, что больше 25.

Сколько клеток может посетить муравей, если его начальная позиция (1000,1000), (включая начальную клетку)?
"""

# == 148848 301566 (21.67s)

import collections as C
import itertools   as I


START_X = 1000
START_Y = 1000
SUM_THRESHOLD = 25


cells = set()  # {(x, y)}
todo  = set()  # {(x, y)}
seenlines = C.defaultdict(set)  # y -> {x}


def numsum(x, y):
	assert 0 <= x and 0 <= y, (x, y)
	return sum(map(int, ''.join(map(str, (x, y)))))


def checkcell(x, y):
	return numsum(x, y) <= SUM_THRESHOLD


def scanline(ox, oy):
	for x1 in I.count(ox-1, -1):
		if not checkcell(x1, oy):
			break

	for x2 in I.count(ox+1):
		if not checkcell(x2, oy):
			break

	cells.update((x, oy) for x in range(x1 + 1, x2))
	return list(range(x1 + 1, x2))


todo = set([(START_X, START_Y)])

while todo:
	ox, oy = todo.pop()
	seenlines[oy].add(ox)

	if checkcell(ox, oy):
		line = scanline(ox, oy)
		seenlines[oy].update((x, oy) for x in line)
		todo.update(set((x, oy + 1) for x in line) - seenlines[oy + 1])
		todo.update(set((x, oy - 1) for x in line) - seenlines[oy - 1])


print('==', len(cells), sum(map(len, seenlines.values())))

allx = set(x for x, y in cells)
ally = set(y for x, y in cells)

print('  ', '{}..{}'.format(min(allx), max(allx)), '{}..{}'.format(min(ally), max(ally)))
