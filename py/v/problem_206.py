#!/usr/bin/python
 
#1_2_3_4_5_6_7_8_9_0
 
import math
from decimal import *
 
def solve():
 
  template = ['1','2','3','4','5','6','7','8','9','0']
 
  n = 99999999
  while n > 0:
 
    # in numero da incastrare termina con 0
    incastro = list('{:08d}0'.format(n)) 
    result = [None]*(len(template)+len(incastro))
    result[::2] = template
    result[1::2] = incastro
    s = Decimal(long(''.join(result)))
    #un quadrato perfetto e congruo a 0 o a 1 modulo 3
    m = s % Decimal(3) 
    if m == 0 or m == 1:
      sr = s.sqrt()
      if (sr - sr.to_integral_exact(rounding=ROUND_FLOOR)) == 0.0:
        return sr
     
    n -= 1
 
  return False
 
race = {
	'author': 'valeria',
	'problemName': '206',
	'raceables': { 
		'brute': solve,
	}  
}

if __name__ == "__main__":
	print solve()