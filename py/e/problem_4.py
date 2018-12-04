#!/usr/bin/env python
# -*- coding: utf-8 -*-

# A palindromic number reads the same both ways. The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 × 99.
# Find the largest palindrome made from the product of two 3-digit numbers.
import itertools
import functools

def is_palindrome(n):
    str_n = str(n)
    for i in range(0,len(str_n)//2):
        if str_n[i] != str_n[len(str_n)-i-1]:
            return False
    return True

def from_digits_list_to_string(digits):
    return functools.reduce(lambda a, b: str(a) + str(b), digits, "")

def euler(n):
    digits = list(reversed(range(10)))
    n_digits_numbers = [from_digits_list_to_string(i) for i in itertools.product(digits, repeat=n)]

    solution_components = []
    max_palindrome = 0

    for i in itertools.product(n_digits_numbers, n_digits_numbers):
        product = int(i[0]) * int(i[1])
        if product>max_palindrome and is_palindrome(product):
            max_palindrome = product
            solution_components = i

    return max_palindrome, solution_components

def solve(n=3):
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