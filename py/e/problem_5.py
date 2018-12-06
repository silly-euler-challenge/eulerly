#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.
# What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?

def is_divisible_by_all_integers_below(i, n):
    for j in range(n, 0, -1):
        if i % j != 0:
            return False
    return True

def euler(n):
    i=n
    while not is_divisible_by_all_integers_below(i, n):
        i += 1
    return i

def solve(n=20):
    return euler(n)

race = {
    'problemName': '3',
    'author': 'erik',
    'raceables': {
        'solution':  solve
    }
}

if __name__ == "__main__":
    print solve()
