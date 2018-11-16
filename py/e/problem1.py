#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://projecteuler.net/problem=1
# If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.
# Find the sum of all the multiples of 3 or 5 below 1000.


def sum(n,m):
    return (n * (n+m)) // (2*m)

def euler(n):
    n=n-1
    n3 = max(n-n%3, 0)
    n5 = max(n - n%5, 0)
    n15 = max(n - n%15, 0)
    return sum(n3, 3) + sum(n5, 5) - sum(n15, 15)

def solve(n=1000):
    return euler(n)

# export to be measured
race = {
    'problemName': '1',
    'author': 'erik',
    'raceables': {
        'solution': solve
    }
}

if __name__ == "__main__":
    print solve()


