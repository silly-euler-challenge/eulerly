#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Find the unique positive integer whose square has the form 1_2_3_4_5_6_7_8_9_0,
# where each “_” is a single digit.
 
import time

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

# take 2

from decimal import *

def from_above():
	return find(99999999, -1)

def from_below():
	return find(0, 1)

def find(start, direction):
	m = start
	while True:
		ms = '%08d' % m
		n = long('1%s2%s3%s4%s5%s6%s7%s8%s900' % (ms[0], ms[1], ms[2], ms[3], ms[4], ms[5], ms[6], ms[7]))

		# check if it's a square.
		mod3 = n % 3
		if mod3 == 1 or mod3 == 0:
			root = Decimal(n).sqrt()
			if root - root.to_integral_exact(rounding=ROUND_FLOOR) == 0.0:
				return root

		m = m + direction


#
# Chores
#
race = {
    'problemName': '206',
    'author': 'marco',
    'raceables': { 
    	#'naive': naive,            ## too slow... 5 mins
    	#'from_above': from_above,  ## too slow...
    	'from_below': from_below    ## best of all of them.
    }
}

if __name__ == "__main__":
	print take2()
    