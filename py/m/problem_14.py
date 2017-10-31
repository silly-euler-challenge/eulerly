#!/usr/bin/env python
# -*- coding: utf-8 -*-

def collatz_len(n, known_lengths):
	seq_len = 0
	m = n
	while m != 1:
		if m in known_lengths:
			seq_len = seq_len + known_lengths[m]
			known_lengths[n] = seq_len
			return seq_len, known_lengths
		if (m % 2 == 0):
			m //= 2
		else:
			m = (3 * m + 1) / 2 # thanks valeria.
		seq_len += 1
	known_lengths[n] = seq_len + 1 # +1 here is for the last one on the sequence
	return seq_len, known_lengths

def solve_up(n=999999):
	max_i, max_len = 1, 1
	known_len = {}
	for i in xrange(2, n + 1):
		len_i, known_len = collatz_len(i, known_len)
		if len_i > max_len:
			max_i, max_len = i, len_i
	return max_i

def solve_down(n=999999):
	max_i, max_len = 1, 1
	known_len = {}
	for i in xrange(n, 1, -1):
		len_i, known_len = collatz_len(i, known_len)
		if len_i > max_len:
			max_i, max_len = i, len_i
	return max_i

###########################
# brute implementation
###########################

def collatz_len2(n):
	seq_len = 1
	while n != 1:
		if (n % 2 == 0):
			n //= 2
		else:
			n = 3 * n + 1
		seq_len += 1
	return seq_len

def brute(n=999999):
	key_func = lambda item: item[1]
	return max(map(lambda i: (i, collatz_len2(i)), range(1, n + 1)), key=key_func)

race = {
    'problemName': '14',
    'author': 'marco',
    'raceables': { 
        'speranze-di-riscatto-insu': solve_up,
        'speranze-di-riscatto-ingiù': solve_down,
        'disperazione': brute
    }
}

if __name__ == "__main__":
	print solve()
    