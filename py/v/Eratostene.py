import math

def Eratostene(N=1000000):
	setaccio = range(2,N)
	for i in range(2,(int)(math.sqrt(N))+1):
		setaccio = list(filter((lambda x: (x%i!=0 or x==i)), setaccio))			
	return setaccio

def Eratostene2(N=1000000):
	setaccio = filter((lambda x: (x%2!=0 or x==2)), range(2, N))
	sqrt_n = int(math.sqrt(N)) + 1
	for i in xrange(3, sqrt_n, 2):
		setaccio = filter((lambda x: (x%i!=0 or x==i)), setaccio)
	return setaccio

def NonEraTostene(n=1000000):
	primi = [2]
	len_primi = 1
	for i in xrange(3, n, 2):
		sqrt_of_i = int(math.sqrt(i)) + 1
		k = 0
		is_prime = True
		while k < len_primi and (primi[k] <= sqrt_of_i):
			if i % primi[k] == 0:
				is_prime = False
			k += 1

		if is_prime:
			primi.append(i)
			len_primi += 1

	return primi

#
# Generator version
#

def primes_xrange(nth_prime):
	'''Like xrange(n) but gives you the first n primes'''
	primi = [2]
	len_primi = 1

	if nth_prime <= 0:
		return

	yield 2
	if nth_prime == 1:	
		return

	i = 3
	while len_primi < nth_prime:
		sqrt_of_i = int(math.sqrt(i)) + 1
		k = 1
		is_prime = True
		while k < len_primi and (primi[k] <= sqrt_of_i):
			if i % primi[k] == 0:
				is_prime = False
			k += 1

		if is_prime:
			primi.append(i)
			len_primi += 1
			yield i

		i+=2

def prime_factors(n):
	'''
	Returns the list of prime factors and their exponent, e.g. for 144 returns ([2, 3], [4, 2]) meaning 2^4 * 3^2
	'''
	p_facts = []
	exponents = []
	for p in primes_xrange(n // 2):
		exp = 0
		while (n % p == 0):
			n //= p
			exp += 1
			p_facts.append(p)
		exponents.append(exp)
		if n == 1:
			break
	return list(set(p_facts)), exponents


race = {
    'problemName': 'eratostene',
    'author': 'valeria & marco',
    'raceables': { 
        'eratostene_uno': Eratostene,
        'eratostene_due': Eratostene2,
        'non_era_tostene': NonEraTostene
    }  
}

if __name__ == '__main__':
	un_milione = 1000000
	Eratostene(un_milione)
	Eratostene2(un_milione)
	NonEraTostene(un_milione)
