#!/usr/bin/env python 

def pairs(seq):
	'''Iterates over a sequence in adjacent pairs'''
	i = iter(seq)
	prev = next(i)
	for item in i:
		yield prev, item
		prev = item

def pairwise_sums(current_row):
	'''Given a list of numbers, return a list of the sums of every adjacent pairs in the list'''
	next_row = [1]
	for a, b in pairs(current_row):
		next_row.append(a + b)
	next_row.append(1)
	return next_row

def tartaglia_row(n):
	if n == 0:
		return [1]
	elif n == 1:
		return [1, 1]
	else:
		row = [1, 1]
		for i in xrange(n-1):
			row = pairwise_sums(row)
		return row

def count_paths(n=20):
	# all_possible_paths = 2^(2n)
	# target_probability = tartaglia_row(2 * n)[n] / 2^(2n)
	# paths_to_target = all_possible_paths * target_probability -> simplify the 2^(2n), it remains just the central term of the tartaglia row.
	return tartaglia_row(2 * n)[n]

from math import factorial as fact

def binomial_coeff(n=20):
	fact_n = fact(n)
	return fact(2 * n) / (fact_n * fact_n)

race = {
    'problemName': '15',
    'author': 'marco',
    'raceables': { 
        'tar...tar...tartaglia': count_paths,
        'il cerchio si chiude': binomial_coeff
    }
}


