#!/usr/bin/env python
# -*- coding: utf-8 -*-

data = '''
08 02 22 97 38 15 00 40 00 75 04 05 07 78 52 12 50 77 91 08
49 49 99 40 17 81 18 57 60 87 17 40 98 43 69 48 04 56 62 00
81 49 31 73 55 79 14 29 93 71 40 67 53 88 30 03 49 13 36 65
52 70 95 23 04 60 11 42 69 24 68 56 01 32 56 71 37 02 36 91
22 31 16 71 51 67 63 89 41 92 36 54 22 40 40 28 66 33 13 80
24 47 32 60 99 03 45 02 44 75 33 53 78 36 84 20 35 17 12 50
32 98 81 28 64 23 67 10 26 38 40 67 59 54 70 66 18 38 64 70
67 26 20 68 02 62 12 20 95 63 94 39 63 08 40 91 66 49 94 21
24 55 58 05 66 73 99 26 97 17 78 78 96 83 14 88 34 89 63 72
21 36 23 09 75 00 76 44 20 45 35 14 00 61 33 97 34 31 33 95
78 17 53 28 22 75 31 67 15 94 03 80 04 62 16 14 09 53 56 92
16 39 05 42 96 35 31 47 55 58 88 24 00 17 54 24 36 29 85 57
86 56 00 48 35 71 89 07 05 44 44 37 44 60 21 58 51 54 17 58
19 80 81 68 05 94 47 69 28 73 92 13 86 52 17 77 04 89 55 40
04 52 08 83 97 35 99 16 07 97 57 32 16 26 26 79 33 27 98 66
88 36 68 87 57 62 20 72 03 46 33 67 46 55 12 32 63 93 53 69
04 42 16 73 38 25 39 11 24 94 72 18 08 46 29 32 40 62 76 36
20 69 36 41 72 30 23 88 34 62 99 69 82 67 59 85 74 04 36 16
20 73 35 29 78 31 90 01 74 31 49 71 48 86 81 16 23 57 05 54
01 70 54 71 83 51 54 69 16 92 33 48 61 43 52 01 89 19 67 48
'''

def as_int_matrix(string_grid):
	'''From grid of numbers (separated by whitespace and end of lines) to a matrix of ints'''
	# pesky empty lines...
	return map(lambda line: map(int, line.split()), filter(lambda line: len(line) > 0, string_grid.splitlines()))

#############################################################################
#
# Take 1, simple, but naive.
# 
#############################################################################

# possible directions for walking the matrix
EAST = 0, 1
SOUTH_EAST = 1, 1
SOUTH = 1, 0
NORTH_EAST = -1, 1

def next_pos(start_pos, direction, offset):
	'''Gives the next coordinates in a particular direction'''
	x, y = start_pos
	dir_x, dir_y = direction
	return x + offset * dir_x, y + offset * dir_y

def win_prod(matrix, n, start_pos, direction, win_len):
	'''Calculates the product of a window in a certain direction from a given starting point'''
	p = 1
	for offset in xrange(win_len):
		x, y = next_pos(start_pos, direction, offset)
		if x < 0 or y < 0 or x >= n or y >= n: # don't go over the edges of the matrix...
			break
		p *= matrix[x][y]
	return p

def coords(n):
	for i in xrange(n):
		for j in xrange(n):
			yield i, j

def simple(string_grid=data, win_len=4):
	matrix = as_int_matrix(string_grid)
	n = len(matrix) # assume it's square.

	max_prod = 0
	for i, j in coords(n):
		pos = (i, j)
		p1 = win_prod(matrix, n, pos, EAST, win_len)
		p2 = win_prod(matrix, n, pos, SOUTH_EAST, win_len)
		p3 = win_prod(matrix, n, pos, EAST, win_len)
		p4 = win_prod(matrix, n, pos, NORTH_EAST, win_len)
		max_prod = max(max_prod, p1, p2, p3, p4)
	return max_prod

#############################################################################
#
# Take 2, avoiding calculating the prods when there is a zero factor.
#
#############################################################################

# circular buffers are taken from problem 8.
class CircularBuffer:
	def __init__(self, size):
		self.size = size
		self.data = [0 for x in xrange(size)]
		self.oldest = 0 # points to the oldest item in the buffer (i.e. the first one to overwrite when a new factor arrives)

	def add(self, item):
		removed = self.data[self.oldest]
		self.data[self.oldest] = item
		self.oldest = (self.oldest + 1) % self.size
		return removed

class CircularProductBuffer:
	def __init__(self, size):
		self.buf = CircularBuffer(size)
		self.max_prod = 0
		self.current_prod = 1
		self.zeros = size

	def add(self, item):
		'''Divide for what's leaving the buffer, multiply by what's entering, and take care of zeros'''
		removed = self.buf.add(item)
		if item:
			self.current_prod *= item
		else:
			self.zeros += 1
		if removed:
			self.current_prod /= removed
		else:
			self.zeros -= 1
		if not self.zeros:
			self.max_prod = max(self.max_prod, self.current_prod)

GO_EAST = 0, 1
GO_SOUTH_EAST = 1, 1
GO_SOUTH = 1, 0
GO_NORTH_EAST = -1, 1

# Trails generator. Each generator yields the starting coord of the trails, the lentgh of the trail
# and the direction in which to go.
def diags_south_east(n, win_len):
	'''yields starting pos and len of the trail'''
	yield 0, 0, n, GO_SOUTH_EAST
	for k in xrange(1, n):
		yield 0, k, n - k, GO_SOUTH_EAST
		yield k, 0, n - k, GO_SOUTH_EAST

def diags_north_west(n, win_len):
	'''yields starting pos and len of the trail'''
	yield n - 1, 0, n, GO_NORTH_EAST
	for k in xrange(1, n):
		yield n - 1 - k, 0, n - k, GO_NORTH_EAST
		yield n - 1, k, n - k, GO_NORTH_EAST

def horizontal_trails(n, win_len):
	for k in xrange(n):
		yield k, 0, n, GO_EAST

def vertical_trails(n, win_len):
	for k in xrange(n):
		yield 0, k, n, GO_SOUTH

def max_on_trails(matrix, n, trail_generator, win_len):
	max_prod = 0
	for x0, y0, length, direction in trail_generator(n, win_len):
		buf = CircularProductBuffer(win_len)
		dx, dy = direction
		for offset in xrange(length):
			x, y = x0 + offset * dx, y0 + offset * dy
			factor = matrix[x][y]
			buf.add(factor)
		max_prod = max(max_prod, buf.max_prod)
	return max_prod

def better(string_grid=data, win_len=4):
	matrix = as_int_matrix(string_grid)
	n = len(matrix) # assume it's square.
	# For all trails, walk them feeding items in circular buffers and getting the max prod out of them.
	m1 = max_on_trails(matrix, n, horizontal_trails, win_len)
	m2 = max_on_trails(matrix, n, vertical_trails, win_len)
	m3 = max_on_trails(matrix, n, diags_south_east, win_len)
	m4 = max_on_trails(matrix, n, diags_north_west, win_len)
	return max(m1, m2, m3, m4)

#
# Chores
#
race = {
    'problemName': '11',
    'author': 'marco',
    'raceables': { 
        'simple': simple, 
        'better': better
    }
}

if __name__ == "__main__":
	print(simple())
	print(better())

    