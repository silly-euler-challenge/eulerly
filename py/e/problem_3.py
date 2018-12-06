#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://projecteuler.net/problem=3
# The prime factors of 13195 are 5, 7, 13 and 29.
# What is the largest prime factor of the number 600851475143 ?

def is_prime(n):
    if n <= 3:
        return n > 1
    elif n % 2 == 0 or n % 3 == 0:
        return False
    i=5
    while i*i <= n:
        if n % i == 0 or n % (i+2) == 0:
            return False
        i = i + 6
    return True

def euler(n):
    factors = []
    i = 1
    while n != 1 :
        i += 1
        if n % i == 0 and is_prime(i):
            factors.append(i)
            n //= i
    return factors

def solve(n=600851475143):
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