#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Написать функцию, строящую дерево по списку пар `id` (`id` родителя, `id` потомка),
где `None` - `id` корневого узла.
"""

class InfiniteLoop(Exception):
	pass


def to_tree(source):
	def build_node(parent, trace):
		node = {}

		for key, child in source:
			if key != parent:
				continue
			if child is None:
				raise ValueError('Child can\'t be None')
			if (key, child) in trace:
				raise InfiniteLoop((key, child), trace)  # @note: `trace is list` для сохранения порядка при выводе ошибки
			node[child] = build_node(child, trace + [(key, child)])

		return node

	return build_node(None, [])


def default_test():
	source = [
		(None, 'a'),
		(None, 'b'),
		(None, 'c'),
		('a',  'a1'),
		('a',  'a2'),
		('a2', 'a21'),
		('a2', 'a22'),
		('b',  'b1'),
		('b1', 'b11'),
		('b11', 'b111'),
		('b',  'b2'),
		('c',  'c1'),
	]

	expected = {
		'a': {'a1': {}, 'a2': {'a21': {}, 'a22': {}}},
		'b': {'b1': {'b11': {'b111': {}}}, 'b2': {}},
		'c': {'c1': {}},
	}

	result = to_tree(source)

	import pprint
	print('--- result ---')
	pprint.pprint(result)
	print('--- expected ---')
	pprint.pprint(expected)

	assert result == expected


if __name__ == '__main__':
	default_test()
