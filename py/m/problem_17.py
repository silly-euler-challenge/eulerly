#!/usr/bin/env python

# If the numbers 1 to 5 are written out in words: one, two, three, four, five,
# then there are 3 + 3 + 5 + 4 + 4 = 19 letters used in total.
# If all the numbers from 1 to 1000 (one thousand) inclusive were written out in words,
# how many letters would be used?
# NOTE: Do not count spaces or hyphens.
# For example, 342 (three hundred and forty-two) contains 23 letters and 115 (one hundred and fifteen)
# contains 20 letters. The use of "and" when writing out numbers is in compliance with British usage.


def make_words():
    words = {
        0: '',
        1: 'one',
        2: 'two',
        3: 'three',
        4: 'four',
        5: 'five',
        6: 'six',
        7: 'seven',
        8: 'eight',
        9: 'nine',
        10: 'ten',
        11: 'eleven',
        12: 'twelve',
        13: 'thirteen',
        14: 'fourteen',
        15: 'fifteen',
        16: 'sixteen',
        17: 'seventeen',
        18: 'eighteen',
        19: 'nineteen',
        20: 'twenty',
        30: 'thirty',
        40: 'forty',
        50: 'fifty',
        60: 'sixty',
        70: 'seventy',
        80: 'eighty',
        90: 'ninety',
        1000: 'one thousand'
    }

    for n1 in xrange(0, 10):
        for n100 in xrange(0, 100):
            n = n1 * 100 + n100
            if n in words:
                continue
            if n % 100 == 0:
                words[n] = words[n1] + ' hundred'
            elif n % 10 == 0:
                words[n] = words[n1] + ' hundred and ' + words[n100]
            elif n < 100:
                decs = (n // 10) * 10
                units = n % 10
                words[n] = words[decs] + '-' + words[units]
            else:
                words[n] = words[n1] + ' hundred and ' + words[n100]
    return words


def solve():
    words = make_words()
    out = 0
    for n in xrange(1, 1000 + 1):
        out += len(words[n].replace(' and ', '').replace('-', '').replace(' ', ''))
    return out


race = {
    'problemName': '17',
    'author': 'marco',
    'raceables': {
        'boh': solve
    }
}

if __name__ == "__main__":
    print solve()
