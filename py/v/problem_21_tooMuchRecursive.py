#!/usr/bin/python

import math 

def genera_primi(N, primi):
  '''
  Genera il numeri primi inferiori a N
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
	esponenti = {}
	divisori = []
	somma = - N
	for p in primi:
		while(N % p == 0):
			N = N/p
			if p in esponenti:
				esponenti[p] += 1
				divisori.append(p**esponenti[p])				
				somma += p**esponenti[p]
				
				for key in esponenti:
					if key != p:
						somma += reduce(lambda x, y: x + y, map(lambda x: key**x * p**esponenti[p], range(1,esponenti[key]+1)))
				
				if somma > 10000 :
					return 0
			else:
				esponenti[p] = 1
				divisori.append(p)
				if len(divisori) > 1:
					somma +=  reduce(lambda x, y: x + y, map(lambda x: x * p, divisori[0:-1])) + p
				else:
					somma += p
				if somma > 10000 :
					return 0

	return somma
  	    	

def cerca_un_amico(N, amici, gia_visti, primi):

	gia_visti.append(N)
	primi = genera_primi(N, primi)
	amico = calcola_somma_divisori(N, primi)
	x = 0
	if amico not in gia_visti:
		if amico > N:
			primi = genera_primi(amico, primi)
		x = calcola_somma_divisori(amico, primi)
	#se ho gia cercato amici per amico cerco altre coppie di amici tra quelli non ancora visti. Se ho esaurito i numeri ritorno la lista di amici
	else:
		for i in xrange(1,10000) :
			if i not in gia_visti :
				return cerca_un_amico(i, amici, gia_visti, primi)
		return amici
		
	
	#ho trovato un amico! Li aggiungo alla lista di amici, e alla lista di numeri visti
	if N == x:
		amici.append(N)
		amici.append(amico)
		gia_visti.append(amico)
		#Cerco altre coppie di amici, tra quelli non ancora visti. Se ho esaurito i numeri ritorno la lista di amici
		for i in xrange(1,10000) :
			if i not in gia_visti :
				return cerca_un_amico(i, amici, gia_visti, primi)
		return amici

	#N non ha amici. Cerco un amico per amico
	else:
		return cerca_un_amico(amico, amici, gia_visti, primi)


def solve():
	amici = []
	gia_visti = []
	primi = []
	amici = cerca_un_amico(1, amici, gia_visti, primi)
	return amici
	
	
amici = solve()
print "amici", amici