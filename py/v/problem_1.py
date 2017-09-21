#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://projecteuler.net/problem=1
# If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.
# Find the sum of all the multiples of 3 or 5 below 1000.

def solve():
	blocchetto = 195 #somma dei multipli di 3 e/o di 5 minori di 30
	somma = blocchetto

	for item in range(1,33):
		blocchetto = blocchetto+30*14
		somma = somma + blocchetto
	
	somma = somma +990+993+995+996+999
	
	return somma

race = {
	'author': 'valeria',
	'problemName': '1',
	'raceables': { 
		'blocchetto': solve
	}  
}

if __name__ == "__main__":
    print solve()
    
