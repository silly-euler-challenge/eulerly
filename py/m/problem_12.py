#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from Eratostene import prime_factors

def triang_nums2():
	n = 3
	while True:
		yield n * (n - 1) // 2
		n += 1

def triang_nums():
	n = 2
	sum = 3
	while True:
		yield sum
		n += 1
		sum += n

def count_divisors(n):
	primes, exp = prime_factors(n)
				  #2) multiply them	  #1) sum 1 to each exponent
	return reduce(lambda a, b: a * b, map(lambda e: e + 1, exp))

def brute(divisors=500, triangulars=triang_nums):
	for t in triangulars():
		if count_divisors(t) > divisors:
			return t

race = {
    'problemName': '12',
    'author': 'marco',
    'raceables': { 
        'brutto-forte': brute
    }
}

if __name__ == "__main__":
	print simple()

    