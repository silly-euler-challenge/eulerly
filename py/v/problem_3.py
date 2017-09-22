def genera_primo(primo, primi):
	'''
	Genera il (primo) numero primo successivo a "primo" (uhmmmm...)
	La lista "primi" tiene in memoria tutti i numeri primi calcolati fino a quel momento
	'''
	candidato = primo
	flag = 1
	if candidato == 1 or candidato == 2:
		primi.append(candidato+1)
		return candidato+1, primi

	while flag == 1:
		candidato += 2
		for primo in primi:
			flag = 0
			if(candidato % primo == 0):
				flag == 1
	primi.append(candidato)
	return candidato, primi
	
def calcola_fattore(N):
	'''
	Calcola e stampa i fattori primi di N
	'''
	primi = [1]
	primo = 1
	fattori = [1]
	while primo < N:
		primo, primi = genera_primo(primo, primi)
		while (N % primo == 0):
			fattori.append(primo)
			N = N/primo
	return fattori

def solve():
	return calcola_fattore(600851475143)

race = {
	'author': 'valeria',
	'problemName': '3',
	'raceables': { 
		'blocchetto': solve
	}  
}

if __name__ == "__main__":
    print solve()
