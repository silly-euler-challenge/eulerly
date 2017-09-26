#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The sum of the squares of the first ten natural numbers is,
# 1^2 + 2^2 + ... + 10^2 = 385
# 
# The square of the sum of the first ten natural numbers is,
# (1 + 2 + ... + 10)^2 = 552 = 3025
#
# Hence the difference between the sum of the squares of the first ten natural numbers and the square of the sum is 3025 − 385 = 2640.
#
# Find the difference between the sum of the squares of the first one hundred natural numbers and the square of the sum.



def semi_naive(n=100):
	sum_of_squares = reduce(lambda x, y: x + y, map(lambda x: x**2, range(1, n + 1)))
	square_of_sum = ((n * (n + 1)) / 2) ** 2
	return square_of_sum - sum_of_squares

race = {
    'problemName': '6',
    'author': 'marco',
    'raceables': { 
        'naive': semi_naive
    }  
}

if __name__ == "__main__":
    print solve()