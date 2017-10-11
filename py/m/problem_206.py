#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Find the unique positive integer whose square has the form 1_2_3_4_5_6_7_8_9_0,
# where each “_” is a single digit.

digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

def conforms(n):
	s = str(n)
	if len(s) != 19:
		return False
	for i, d in enumerate(digits):
		if s[2 * i] != d:
			return False
	return True

def naive():
	n = 1000000000 # first n whose square has 19 digits.
	while True:
		n2 = n * n
		if conforms(n2):
			break
		n += 1
	return n

#
# Chores
#
race = {
    'problemName': '206',
    'author': 'marco',
    'raceables': { 
        'boh': naive
    }
}

if __name__ == "__main__":
	print naive()
    