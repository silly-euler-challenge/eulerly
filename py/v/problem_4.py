def solve():
	for digit3 in xrange(999,100,-1):
		digit6 = (int)('%d%s' % (digit3,str(digit3)[::-1]))

		for divisore in xrange(999,100,-1):
			if (digit6 % divisore == 0 and digit6/divisore < 999):
				# print digit6, "divisore: ",divisore
				return digit6
	return 0
  
race = {
	'author': 'valeria',
	'problemName': '4',
	'raceables': { 
		'blocchetto': solve
	}  
}

if __name__ == "__main__":
    print solve()
