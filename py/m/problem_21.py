#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("../v")

from Eratostene import primes_forever


def prime_factors(n):
    '''
    Returns the list of prime factors and their exponent, e.g. for 144 returns ([2, 3], [4, 2]) meaning 2^4 * 3^2
    '''
    p_facts = []
    exponents = []
    for p in primes_forever():
        exp = 0
        while (n % p == 0):
            n //= p
            exp += 1

        if exp > 0:
            p_facts.append(p)
            exponents.append(exp)

        if n == 1:
            break
    return p_facts, exponents


def count_up(max_counters):
    """
    Generator that counts up in sequential fashion.
    Counters is a list of (non-zero) ints that symbolize figures to be counted up, each int is the "base" for
    the corresponding digit, most significant digit is on the left
    Example [1, 1, 1] is equivalent to 3 binary digits
    [2, 1 , 1] is equivalent of having 2 binary digits, followed by a base 3 digits.
    Each time called the generator will yield an array with the current count
    count([2, 1]) will yield [0,0], [0,1], [1,0] [1, 1] [2, 0] [2, 1]
    """
    bases = map(lambda x: x + 1, max_counters)
    lsd = len(bases) - 1  # least significant digit
    current = [0 for item in bases]
    while True:
        current[lsd] += 1

        digit = lsd
        overflow = False
        while current[digit] == bases[digit] and not overflow:
            current[digit] = 0
            digit -= 1
            if digit >= 0:
                current[digit] += 1
            else:
                overflow = True

        if overflow:
            break
        yield current


def proper_divisors(n):
    if n == 1:
        return []
    prime_facts, max_exponents = prime_factors(n)
    facts = [1]
    for exp in count_up(max_exponents):
        f = 1
        for pf, e in zip(prime_facts, exp):
            f *= pf**e
        if f != 1 and f != n:
            facts.append(f)
    return facts


def sum_of_divisors(n):
    return reduce(lambda x, y: x+y, proper_divisors(n), 0)


def amicable_sum_below(n=10000):
    amicables = []
    divsums = {}
    for i in xrange(3, n + 1):
        if i not in divsums:
            friend = sum_of_divisors(i)
            divsums[i] = friend
            if friend <= n:
                if friend not in divsums:
                    friend_of_friend = sum_of_divisors(friend)
                    divsums[friend] = friend_of_friend
                if divsums[friend] == i:
                    amicables.append(i)
                    amicables.append(divsums[friend])
    #print sorted(set(amicables))
    return reduce(lambda x, y: x + y, set(amicables))


def amicables_sum_below2(n=10000):
    friends = {}
    for a in xrange(3, n + 1):
        b = sum_of_divisors(a)
        if b <= n and b != a:
            c = sum_of_divisors(b)
            if c == a:
                friends[a] = b
                friends[b] = a
    # print sorted(friends.keys())
    # print friends
    return reduce(lambda x, y: x + y, friends.keys())



race = {
    'problemName': '21',
    'author': 'marco',
    'raceables': {
        # 'amicables': amicable_sum_below,
        'naive': amicables_sum_below2
    }
}


if __name__ == "__main__":
    nn = [6, 28]
    for n in nn:
        print 'prime factors', n, prime_factors(n)
        print '     divisors', n, proper_divisors(n)
        print '  sum of divs', n, sum_of_divisors(n)

