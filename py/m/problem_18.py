#!/usr/bin/env python
# -*- coding: utf-8 -*-

# By starting at the top of the triangle below and moving to adjacent numbers on the row below, the maximum total from top to bottom is 23.

# 3
# 7 4
# 2 4 6
# 8 5 9 3

# That is, 3 + 7 + 4 + 9 = 23.

# Find the maximum total from top to bottom of the triangle below:
import sys

data = """
75
95 64
17 47 82
18 35 87 10
20 04 82 47 65
19 01 23 75 03 34
88 02 77 73 07 63 67
99 65 04 28 06 16 70 92
41 41 26 56 83 40 80 70 33
41 48 72 33 47 32 37 16 94 29
53 71 44 65 25 43 91 52 97 51 14
70 11 33 28 77 73 17 78 39 68 17 57
91 71 52 38 17 14 91 43 58 50 27 29 48
63 66 04 68 89 53 67 30 73 16 69 87 40 31
04 62 98 27 23 09 70 98 73 93 38 53 60 04 23
"""

def log(*arg):
    print '+++', arg

# NOTE: As there are only 16384 routes, it is possible to solve this problem by trying every route.
# However, Problem 67, is the same challenge with a triangle containing one-hundred rows; it cannot be solved by brute force, and requires a clever method! ;o)

def as_a_triangle_of_ints(data):
    return map(lambda x: map(int, x.split()), filter(lambda x: len(x) > 0, data.splitlines()))


def sorted_indices(seq, reverse=False):
    '''Sort seq and returns the sorted indices'''
    return map(lambda x: x[0], sorted(enumerate(seq), key=lambda x: x[1], reverse=True))


def pairs(seq):
    '''Iterates over a sequence in adjacent pairs'''
    i = iter(seq)
    prev = next(i)
    for item in i:
        yield prev, item
        prev = item


def is_path_legal(path_indices):
    '''
    Given a list of indices, checks if they form a legal path for walking down the triangle
    (i.e. you can only jump to adjacent children on the next level).
    Visual clue to how it works, since we store the tree in a triangular matrix:
    0                                       0
    0 1                                    0 1
    0 1 2      --> is really this -->     0 1 2
    0 1 2 3                              0 1 2 3
    0 1 2 3 4                           0 1 2 3 4 
    So given a index i on one level, you can just go to i o i+1 on the next level.
    '''
    log('is legal?', path_indices)
    for a, b in pairs(path_indices):
        if b != a and b != (a + 1):
            return False
    return True


def vert_slice(matrix, cols):
    '''
    Slices a 2d matrix, returning a vector selecting one element per row.
    For each row, one element is taken at the index specified in the cols list
    E.g. Vertically slicing 
    [[3, 12, 43]
     [23, 34, 54]
     [2, 22, 45]]
    At indices [0, 1, 2] will give you [3, 34, 45]
    '''
    assert len(matrix) == len(cols), 'Number of row in matrix [%d] is not equal to number of column positions [%d]' % (len(matrix), len(cols))
    return [row[col_pos] for row, col_pos in zip(matrix, cols)]


def find_max_sum_path(triangle):

    n = len(triangle)

    # this is the list of indexes of where each max per level is located within triangle
    # e.g.
    # [
    #   [0]             <-- the element at offset 0 is the max of level 0
    #   [1, 0]          <-- the element at offset 1 is the max of level 1
    #   [2, 0, 1]       <-- the element at offset 2 is the max of level 2
    #   [1, 2, 0, 3]    <-- the element at offset 1 is the max of level 3
    #   [..]
    # ]
    max_paths_ii = map(lambda x: sorted_indices(x, reverse=True), triangle)     

    # this is the set of indices for the max paths structure, we start at the top.
    candidate_max_path_ii = [0 for _ in range(n)]
    
    while True:
        candidate_path_ii = vert_slice(max_paths_ii, candidate_max_path_ii)

        if is_path_legal(candidate_path_ii):
            path_items = vert_slice(triangle, candidate_path_ii)
            return reduce(lambda x, y: x + y, path_items)
        else:
            candidate_max_path_ii = next_candidate_max_path(triangle, max_paths_ii, candidate_max_path_ii)
        #log('candidate_max_path_ii', candidate_max_path_ii)



def next_candidate_max_path(triangle, max_paths_ii, candidate_max_path_ii):
    '''
    Mutates candidate_max_path_ii providing the next immediately lower sum candidate path
    '''

    # find the level on which, going to next lower maximum provides the less possible decrease
    level = None                        # the level at which the min decrease happens
    min_level_dec = sys.maxsize         # the actual current min decrease (used only for min finding)
    zero_decreasing_lvls = []           # levels where there are 2 of the same element, thus zero decreasing.
    for lvl, ii in enumerate(candidate_max_path_ii):
        if ii < lvl: # at lvl 3 we have at max 3 items in the row, no sense in looking for the 4th.
            level_dec = triangle[lvl][max_paths_ii[lvl][ii]] - triangle[lvl][max_paths_ii[lvl][ii + 1]]
            if level_dec < min_level_dec:
                if level_dec > 0:
                    min_level_dec = level_dec
                    level = lvl
                else:
                    zero_decreasing_lvls.append(lvl)

    if level is None:
        level = zero_decreasing_lvls.pop()

    candidate_max_path_ii[level] += 1
    return candidate_max_path_ii

def solve():
    triangle = as_a_triangle_of_ints(data)
    return find_max_sum_path(triangle)

#
# Chores
#
race = {
    'problemName': '18',
    'author': 'marco',
    'raceables': { 
        'proud_if_working': solve
    }
}

if __name__ == "__main__":
    print solve()
    