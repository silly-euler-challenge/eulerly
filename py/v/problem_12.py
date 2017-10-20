#!/usr/bin/python
import math

def Eratostene(N):
  '''
  Calcola i numeri primi fino a N applicando il Crivello di Eratostene
  '''
  setaccio = range(2,N)
  for i in range(2,(int)(math.sqrt(N))+1):
    setaccio = list(filter((lambda x: (x%i!=0 or x==i)), setaccio))			
  return setaccio

  
  
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
      for primo in primi:
        flag = 0
        if(candidato % primo == 0):
          flag == 1
    primi.append(candidato)
	
  return primi
  
def triangolare(n):
  '''
  Calcola l'n-esimo numero triangolare applicando la formula di Gauss
  '''
  T = n * (n + 1)/2
  return T 
	
def conta_divisori(t, primi):
  '''
  Conta il numero di divisori del numero triangolare t. 
  '''
  # 1 e t sono sempre divisori di t
  num_divisori = 2
  i = 0
  #esponenti = {}
  esponenti = [0] * len(primi)
  for p in primi:
    while(t % p == 0):
	  t = t/p
	  esponenti[i] += 1
	  #esponenti[str(p)] += 1
	  num_divisori += 1
    i += 1
	
  num_divisori = reduce(lambda x, y: x * y, list(map(lambda x : x+1, esponenti)))
  
  return num_divisori


def solve():
  '''
  Calcola il primo numero triangolare con 500 fattori
  '''
  
  n = 2
  primi = [2,3]
  num_divisori = 1
 
  while (num_divisori != 500):
    n += 1
    t = triangolare(n)
    primi = genera_primi(t,primi)
    num_divisori = conta_divisori(t,primi)
    #print t, " - ", num_divisori
	
  t = triangolare(n-1)
  num_divisori = conta_divisori(t,primi)
 
  return t, num_divisori
 

	
t, ndiv = solve()
print "t: ", t, " - divisori: ", ndiv
