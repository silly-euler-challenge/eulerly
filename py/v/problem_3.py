def range_gen(start,end):
	'''
	Generatore di range: non tiene in memoria tutto il range, ma solo l'ultimo elemento richiesto
	'''
	i=start
	while i < end:
		yield i
		i += 1

def test_primalita(p):
	stop = (int)(p/2)	
	for i in range_gen(2,stop):
		if(p % i == 0):
			return 1 
	return 0

def genera_primo(p):
	'''
	Genera il (primo) numero primo successivo a p
	'''
	candidato = p+2
	while test_primalita(candidato):
		candidato += 2
	return candidato


def calcola_fattore(N):
	'''
	Calcola i fattori primi dell'intero N 
	'''
	primo = 7
	fattori = [1]
	while primo < N:
		primo = genera_primo(primo)
		if (N % primo == 0):
			fattori.append(primo)
			N = N/primo
	return max(fattori)


def solve():

	return calcola_fattore(600851475143)
