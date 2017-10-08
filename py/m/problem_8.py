#!/usr/bin/env python
# -*- coding: utf-8 -*-

N = 7316717653133062491922511967442657474235534919493496983520312774506326239578318016984801869478851843858615607891129494954595017379583319528532088055111254069874715852386305071569329096329522744304355766896648950445244523161731856403098711121722383113622298934233803081353362766142828064444866452387493035890729629049156044077239071381051585930796086670172427121883998797908792274921901699720888093776657273330010533678812202354218097512545405947522435258490771167055601360483958644670632441572215539753697817977846174064955149290862569321978468622482839722413756570560574902614079729686524145351004748216637048440319989000889524345065854122758866688116427171479924442928230863465674813919123162824586178664583591245665294765456828489128831426076900422421902267105562632111110937054421750694165896040807198403850962455444362981230987879927244284909188845801561660979191338754992005240636899125607176060588611646710940507754100225698315520005593572972571636269561882670428252483600823257530420752963450
#   ^  ^         ^   ^

#
# Take 1, calculates all the products, brute forcing it.
# 
def naive(n=N, win_len=13):
    digits = map(int, list(str(n)))
    digit_count = len(digits)

    max_prod = 0
    for x in xrange(digit_count):
        prod = reduce(lambda x, y: x * y, digits[x : x + win_len])
        max_prod = max_prod if max_prod >= prod else prod
    return max_prod

#
# Take 2, using a circular buffer and avoiding calculating the prod if not necessary.
# Idea is that you mult by what's incoming into the buffer and divide by what's getting out.
# (but you have to take care of zeros)
#
class CircularBuffer:
    def __init__(self, size):
        self.size = size
        self.data = [0 for x in xrange(size)]
        self.oldest = 0 # points to the oldest item in the buffer (i.e. the first one to overwrite when a new factor arrives)

    def add(self, item):
        removed = self.data[self.oldest]
        self.data[self.oldest] = item
        self.oldest = (self.oldest + 1) % self.size
        return removed

class CircularProductBuffer:
    def __init__(self, size):
        self.buf = CircularBuffer(size)
        self.max_prod = 0
        self.current_prod = 1
        self.zeros = size

    def add(self, item):
        '''Divide for what's leaving the buffer, multiply by what's entering, and take care of zeros'''
        removed = self.buf.add(item)

        if item:
            self.current_prod *= item
        else:
            self.zeros += 1

        if removed:
            self.current_prod /= removed
        else:
            self.zeros -= 1

        if not self.zeros:
            self.max_prod = max(self.max_prod, self.current_prod)

    def prod(self):
        return 0 if self.zeros > 0 else self.current_prod

def better(n=N, win_len=13):
    digits = map(int, list(str(n)))
    digit_count = len(digits)
    buf = CircularProductBuffer(win_len)
    for factor in digits:
        buf.add(factor)
    return buf.max_prod

race = {
    'problemName': '8',
    'author': 'marco',
    'raceables': { 
        'naive': naive,
        'better': better
    }  
}

if __name__ == "__main__":
    print solve()