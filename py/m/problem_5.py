#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.
# What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?

def is_prime(n):
    if n % 2 == 0:
        return False
    i = 3
    half_n = n // 2
    while i < half_n:
        if n % i == 0:
            return False
        i += 2
    return True;


def factorize(n):
	factors = [1]

	m = n
	while m % 2 == 0:
		m //= 2
		factors.append(2)

	i = 3
	while m > 1:
		while (m % i == 0) and is_prime(i):
			m //= i
			factors.append(i)
		i += 2
	return factors



def mcm_fact(factors_a, factors_b):
	'''
	Min common multiple from factorized representation. 
	'''
	# ex.
	# 2 2 3 5 7
	# 2 3 5 7 9

	mcm_factors = []
	len_a = len(factors_a)
	len_b = len(factors_b)

	ia = 0
	ib = 0
	while ia < len_a and ib < len_b:
		if factors_a[ia] < factors_b[ib]:
			mcm_factors.append(factors_a[ia])
			ia += 1

		elif factors_a[ia] > factors_b[ib]:
			mcm_factors.append(factors_b[ib])
			ib += 1

		else: # == 
			mcm_factors.append(factors_a[ia]) # both are the same
			ia += 1
			ib += 1

	while ia < len_a:
		mcm_factors.append(factors_a[ia])
		ia += 1

	while ib < len_b:
		mcm_factors.append(factors_b[ib])
		ib += 1

	return mcm_factors


def solve():
	nums = range(1, 20 + 1)
	factors = map(factorize, nums)
	mcm_factors = reduce(mcm_fact, factors, [])
	return reduce(lambda x, y: x * y, mcm_factors)

race = {
    'problemName': '5',
    'author': 'marco',
    'raceables': { 
        'simple': solve
    }  
}

if __name__ == "__main__":
    print solve()