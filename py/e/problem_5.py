#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.
# What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?

#### problem 3
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

def euler3(n):
    factors = []
    i = 1
    while n != 1 :
        i += 1
        if n % i == 0 and is_prime(i):
            factors.append(i)
            n //= i
    return factors
####

def is_divisible_by_all_integers_below(i, n):
    for j in range(n, 0, -1):
        if i % j != 0:
            return False
    return True

def euler_naive(n):
    i=n
    while not is_divisible_by_all_integers_below(i, n):
        i += 1
    return i

def euler_better(n):
    candidate = 1
    max_divider_all = 1
    factors = list(range(1,n+1))

    while max_divider_all <= n:
        new_candidate = candidate
        index = 0
        while not is_divisible_by_all_integers_below(new_candidate, max_divider_all):
            new_candidate = candidate * factors[index]
            index += 1
        candidate = new_candidate
        max_divider_all += 1

    return candidate

def naive(n=20):
    return euler_naive(n)

def solve(n=20):
    return euler_better(n)

race = {
    'problemName': '3',
    'author': 'erik',
    'raceables': {
        'naive':  naive,
        'better':  solve
    }
}

if __name__ == "__main__":
    print solve(20)
