#!/usr/bin/env python
# -*- coding: utf-8 -*-

# A palindromic number reads the same both ways. The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 × 99.
# Find the largest palindrome made from the product of two 3-digit numbers.

##############
# ???
##############

def pal(num):
    return int("%d%s" % (num, str(num)[::-1]))

def naive_w_strings():
    for i in xrange(999, 99, -1): # from 999 to 100
        palindrome = pal(i)
        for div1 in xrange(999, 99, -1):
            if palindrome % div1 == 0:
                div2 = palindrome // div1
                if div2 < 1000 and div2 > 99:
                    return [palindrome, div1, div2, div1 * div2]
    return -1 # :(

race = {
    'problemName': '4',
    'author': 'marco',
    'raceables': { 
        'naive_w_strings': naive_w_strings
    }  
}

if __name__ == "__main__":
    print solve()