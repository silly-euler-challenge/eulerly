#!/usr/bin/env python
# -*- coding: utf-8 -*-

# By starting at the top of the triangle below and moving to adjacent numbers on the row below, the maximum total from top to bottom is 23.

# 3
# 7 4
# 2 4 6
# 8 5 9 3

# That is, 3 + 7 + 4 + 9 = 23.

# Find the maximum total from top to bottom of the triangle below:

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

def as_int_triangle(data):
    return map(lambda x: map(int, x.split()), filter(lambda x: len(x) > 0, data.splitlines()))

def solve(data=data):
    upside_down_triangle = reversed(as_int_triangle(data))
    reduce_top_rows = lambda top, bot: [vert + max(top[i], top[i + 1]) for i, vert in enumerate(bot)]
    return reduce(reduce_top_rows, upside_down_triangle)

#
# Chores
#
race = {
    'problemName': '18',
    'author': 'marco',
    'raceables': { 
        'proud': solve
    }
}

if __name__ == "__main__":
    print solve()
    