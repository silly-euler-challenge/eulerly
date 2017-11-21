#!/usr/bin/python

import math 

def genera_primi(N, primi):
  '''
  Genera i numeri primi inferiori a N
  La lista "primi" tiene in memoria tutti i numeri primi calcolati fino a quel momento
  '''

  if (len(primi) == 0) :
	primi.append(2)
	primi.append(3)
	
  candidato = primi[-1]
	
  while (candidato < N):
    flag = 1
    while flag == 1:
      candidato += 2
      flag = 0
      for primo in primi:
        if(candidato % primo == 0):
          flag = 1
    primi.append(candidato)
	
  return primi
  
def calcola_somma_divisori(N, primi):
	'''
	Calcola la somma dei divisori propri di N. Se la somma supera 10000 la funzione termina e restituisce 0
	'''
	#Una dizionario contentente le coppie "numero primo" - "esponente massimo che divide N"
	esponenti = {}
	#Una lista dei divisori di N
	divisori = []
	somma = - N #brutto!
	
	for p in primi:
		while(N % p == 0):
			N = N/p
			
			#p divide N. Se p e' gia' tra i primi che divide N allora incremento l'esponente, aggiorno la lista dei divisori di N e aggiorno la somma parziale.
			if p in esponenti:
				esponenti[p] += 1
				divisori.append(p**esponenti[p])				
				somma += p**esponenti[p]
				
				#Aggiungo alla somma i prodotti di p**esponenti[p] con tutti gli altri divisori di N, escluse le altre potenze di p:
				for key in esponenti:
					if key != p:
						somma += reduce(lambda x, y: x + y, map(lambda x: key**x * p**esponenti[p], range(1,esponenti[key]+1)))
				#Se la somma parziale supera 10000 allora la ricerca dei divisori termina.
				if somma > 10000 :
					return 10000
					
			#p divide N. Se p non e' tra i numeri primi trovati che dividono N allora lo aggiungo al dizionario degli esponenti, lo aggiungo alla lista dei divisori
			#e aggiorno la somma parziale.
			else:
				esponenti[p] = 1
				divisori.append(p)
				somma += p
				#se ci sono altri divisori, aggiungo alla somma i prodotti di p con tutti gli altri divisori:
				if len(divisori) > 1:
					somma +=  reduce(lambda x, y: x + y, map(lambda x: x * p, divisori[0:-1]))
				#se e' il primo divisore di N che trovo, allora la somma parziale e' banale:
				
				#Se la somma parziale supera 10000 allora la ricerca dei divisori termina.
				if somma > 10000 :
					return 10000
	
	#Se la somma totale supera 10000 allora restituisco 10000.
	if somma > 10000:
		return 10000

	return somma 
	
  
def trova_un_amico(N, primi, gia_visti):
	'''
	trova_un_amico restituisce 0 se non sono riuscita a trovare l'amico di N nel range (1,10000).
	Altrimenti restituisce l'amico di N.
	'''
	primi = genera_primi(N, primi)
	d_N = calcola_somma_divisori(N, primi)
	gia_visti[N] = d_N
	#se la somma d_N supera 10000, non posso trovargli un amico
	if d_N == 10000:
		return 0
	if d_N in gia_visti: # come chiave, non come valore!!
		d_d_N = gia_visti[d_N]
	else: 
		if d_N > N:
			primi = genera_primi(d_N, primi)
		d_d_N = calcola_somma_divisori(d_N, primi)
		gia_visti[d_N] = d_d_N
	
	#ho trovato un amico
	if d_d_N == N:
		return d_N
	#non ho trovato un amico
	return 0
	
 
 
 
def solve() :
 
	primi = []
	#un dizionario che contiene la coppia "numero" - "somma dei suoi divisori"
	gia_visti = {}
	#una lista che contiene i numeri amicabili trovati
	amici = []
 
	for i in xrange(1,10000):
		if i not in gia_visti:
			amico = trova_un_amico(i, primi, gia_visti)
			#ho trovato una coppia di amici
			if amico != 0:
				amici.append(i)
				amici.append(amico)
	return amici
		
	
amici = solve()
print "amici", amici	
		
		
		
		
		
		