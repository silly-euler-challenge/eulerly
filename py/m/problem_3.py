#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The prime factors of 13195 are 5, 7, 13 and 29.
# What is the largest prime factor of the number 600851475143 ?

########################################################
# Take 1, naive
########################################################

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

def factorize(n=600851475143):
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

def solve1(n=600851475143):
    factors = []
    i = 3
    half_n = n // 2
    prod = 1
    while i < half_n:
        if (n % i == 0) and is_prime(i):
            factors.append(i)
            prod *= i

            nn = n // i
            while nn % i == 0:
                nn //= i
                factors.append(i)
                prod *= i

            if prod == n:
                break
        i += 2
    return factors

race = {
    'problemName': '3',
    'author': 'marco',
    'raceables': { 
        'wrong_but_working':  solve1,
        'right_but_slow': factorize
    }  
}

if __name__ == "__main__":
    print solve()