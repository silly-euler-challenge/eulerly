#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from Eratostene import prime_factors, prime_factors2

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

def count_divisors(n, prime_factoring_algo=prime_factors):
	primes, exp = prime_factoring_algo(n)
				  #2) multiply them	  #1) sum 1 to each exponent
	return reduce(lambda a, b: a * b, map(lambda e: e + 1, exp))

def brute(divisors=500, triangulars=triang_nums):
	for t in triangulars():
		if count_divisors(t, prime_factors) > divisors:
			return t

def brute2(divisors=500, triangulars=triang_nums):
	for t in triangulars():
		if count_divisors(t, prime_factors2) > divisors:
			return t


race = {
    'problemName': '12',
    'author': 'marco',
    'raceables': { 
        'brutto-forte': brute,
        'brute2': brute2

    }
}

if __name__ == "__main__":
	print simple()

    