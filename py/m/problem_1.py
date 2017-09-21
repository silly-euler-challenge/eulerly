#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://projecteuler.net/problem=1
# If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.
# Find the sum of all the multiples of 3 or 5 below 1000.

#
# take 1, naive O(n)
#
def solve2(n=1000, a=3, b=5):
    sum = 0
    i = 0
    while i < n:
        if (i % a == 0) or (i % b == 0):
            sum += i
        i += 1
    return sum

#
# take 2, using n (n + 1) / 2 and no loops, O(1)
# 
def sum_of_first_n_ints(n):
    return n * (n + 1) // 2;

def sum_of_mults(n, mult):
    terms = (n // mult) - 1 if n % mult == 0 else n // mult
    return mult * sum_of_first_n_ints(terms)

def solve(n=1000, a=3, b=5):
    return sum_of_mults(n, a) + sum_of_mults(n, b) - sum_of_mults(n, a * b) # assumes a and b have no common factor.

# export to be measured
race = {
    'problemName': '1',
    'author': 'marco',
    'raceables': { 
        'naive': solve2, 
        'good': solve
    }  
}
 

if __name__ == "__main__":
    print solve()
    print solve2()
    
