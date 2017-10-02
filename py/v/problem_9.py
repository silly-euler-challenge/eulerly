import math

def solve():

	'''
	Calcola il prodotto della terna pitagorica (a,b,c) tale che a+b+c = 1000 
	'''
	
	for a in range(1,1000):
		for b in range(a+1,1000):
			for c in range(b+1,1000):
				if(a**2+b**2==c**2 and a+b+c==1000):
					return a*b*c
	return 1
	
	
def solve2():
	for a in xrange(1,1000):
		for b in xrange(a+1, 1000):
			c = 1000-a-b
			if( a**2+b**2 == c**2):
				return a*b*c
	return 1
	
def solve3():
	for c in xrange(500,1,-1):
		for b in xrange(c-1,1,-1):
			a = math.sqrt(c**2-b**2)
			if(a+b+c==1000):
				return a*b*c
	return 1
	
race = {
	'author': 'valeria',
	'problemName': '9',
	'raceables': { 
		'brute': solve
		'insù': solve2
		'ingiù': solve3
	}  
}

if __name__ == "__main__":
  print solve()
  print solve2()
	print solve3()
