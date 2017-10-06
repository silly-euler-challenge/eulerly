#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Eratostene

def simple(n=10001):
    p = None
    for p in Eratostene.primes_xrange(n):
        pass
    return p


race = {
    'problemName': '7',
    'author': 'marco',
    'raceables': { 
        'simple': simple
    }  
}

if __name__ == "__main__":
    print simple()
    