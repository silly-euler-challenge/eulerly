#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Eratostene

def simple(n=2000000):
    return reduce(lambda x, y: x + y, Eratostene.NonEraTostene(n))

race = {
    'problemName': '10',
    'author': 'marco',
    'raceables': { 
        'simple': simple
    }
}

if __name__ == "__main__":
    print simple()
    