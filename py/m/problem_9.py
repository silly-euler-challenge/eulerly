#!/usr/bin/env python
# -*- coding: utf-8 -*-

def naive(n=1000):
    half_n = n // 2
    for a in xrange(1, half_n):
        for b in xrange(a + 1, half_n): # start from a, since b > a
            # use a + b + c = 1000
            c = 1000 - a - b
            if a**2 + b**2 == c**2:
                return a * b * c

race = {
    'problemName': '9',
    'author': 'marco',
    'raceables': { 
        'naive': naive
    }  
}

if __name__ == "__main__":
    print solve()