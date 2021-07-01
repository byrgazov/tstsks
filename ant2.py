#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
На бесконечной координатной сетке находится муравей. Муравей может перемещаться на 1 клетку вверх
(x,y+1), вниз (x,y-1), влево (x-1,y), вправо (x+1,y), по одной клетке за шаг.

Клетки, в которых сумма цифр в координате X плюс сумма цифр в координате Y больше чем 25 недоступны муравью.
Например, клетка с координатами (59, 79) недоступна, т.к. 5+9+7+9=30, что больше 25.

Сколько клеток может посетить муравей, если его начальная позиция (1000,1000), (включая начальную клетку)?
"""

# == 148848 301649 (1.02s)

import collections as C
import itertools   as I

try:
	import PIL
	import PIL.Image
except ImportError:
	PIL = None


START_X = 1000
START_Y = 1000
SUM_THRESHOLD = 25


cells = set()  # {(x, y)}

seen       = C.defaultdict(set)  # y -> {x}
seekup     = C.defaultdict(set)  # y -> {x}
seekdown   = C.defaultdict(set)  # y -> {x}


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


def popseek(seek):
	for y, line in list(seek.items()):
		if line:
			x = line.pop()
			if not seek[y]:
				del seek[y]
			return x, y
		del seek[y]

	raise IndexError('Seek is empty')


line = scanline(START_X, START_Y)
seekup[START_Y]   = set(line)
seekdown[START_Y] = set(line)


while seekup or seekdown:
	if seekup:
		try:
			ox, oy = popseek(seekup)
		except IndexError:
			seekup.clear()
			continue
		dy = +1
	else:
		try:
			ox, oy = popseek(seekdown)
		except IndexError:
			seekup.clear()
			continue
		dy = -1

	oy += dy

	while ox not in seen[oy] and checkcell(ox, oy):
		line = set(scanline(ox, oy))

		seen[oy].update(line)

		seekfwd, seekbwd = (seekup, seekdown) if 0 < dy else (seekdown, seekup)

		# @xxx: есть смутные сомнения по поводу seekbwd

		py = oy - dy
		ny = oy + dy

		if 1 < len(line):
			seekfwd[oy].update(line - seen[ny])
			seekfwd[oy].discard(ox)
			seekbwd[oy].update(line - seen[py])
			seekbwd[oy].discard(ox)

		if py in seekfwd:
			seekfwd[py] -= line

		oy += dy


print('==', len(cells), sum(map(len, seen.values())))

allx = set(x for x, y in cells)
ally = set(y for x, y in cells)
minx, maxx = min(allx), max(allx)
miny, maxy = min(ally), max(ally)

print('  ', '{}..{}'.format(minx, maxx), '{}..{}'.format(miny, maxy))


if PIL is not None:
	width  = maxx - minx + 1
	height = maxy - miny + 1

	data = [0 if (x, y) in cells else int(128 + ((y - miny) / height) * 127)
		for y in range(maxy, minx - 1, -1)
		for x in range(minx, maxx + 1)]
	data = bytes(data)

	with PIL.Image.frombytes('L', (width, height), data) as img:
		img.save('ant.gif')

	print('Image Saved: ant.gif')
