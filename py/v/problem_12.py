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
  esponenti = {}
  for p in primi:
    while(t % p == 0):
	  t = t/p
	  if p in esponenti:
	    esponenti[p] += 1
	  else:
	    esponenti[p] = 1
  
  esponenti = esponenti.values()
  num_divisori = 0
  
  num_divisori = reduce(lambda x, y: x*y, map(lambda x: x+1, esponenti))
  	    
  return num_divisori

def solve():
  '''
  Calcola il primo numero triangolare con 500 fattori
  '''
  
  n = 2
  primi = [2,3]
  num_divisori = 1

  t = 1
  while (num_divisori < 500):
    n += 1
    t = triangolare(n)
    primi = genera_primi(math.sqrt(t)+1,primi)
    num_divisori = conta_divisori(t,primi)
 
  return t, num_divisori
 
 
t, ndiv = solve()
print "t: ", t, " - divisori: ", ndiv

race = {
    'problemName': '12',
    'author': 'valeria',
    'raceables': { 
        'at-last': solve
    }
}

if __name__ == "__main__":
  print solve()

