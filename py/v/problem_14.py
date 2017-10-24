def collatz(n, cammino) :
  if (n == 1):
    return cammino
  if(n % 2 == 0):
    cammino += 1
    return collatz(n / 2, cammino)
  else:
    cammino += 2
    return collatz((3 * n + 1) / 2, cammino)
	
	
def collatz_con_memoria(N, n, cammino_parziale, memoria):
  '''
  N : primissimo punto di partenza della successione
  n : ultimo punto calcolato della successione
  cammino_parziale : lunghezza del cammino fatto fin qui
  memoria : per ogni intero di cui ho calcolato la sequenza, memorizza la lunghezza del cammino corrispondente
  '''
  if(n == 1):
    memoria[N] = cammino_parziale
    return cammino_parziale, memoria
  if(n in memoria):
    memoria[N] = memoria[n]+cammino_parziale
    return cammino_parziale, memoria
  if(n % 2 == 0):
    cammino_parziale += 1
    return collatz_con_memoria(N, n / 2, cammino_parziale, memoria)
  else:
    cammino_parziale += 2
    return collatz_con_memoria(N, (3 * n + 1) / 2, cammino_parziale, memoria)
	
	
def very_brute():

  cammino_max = 0
  n_max = 1
  
  for n in xrange(1,1000000):
    cammino = collatz(n, 0)
    if(cammino > cammino_max):
      cammino_max = cammino
      n_max = n
  return n_max, cammino_max
  
def better():

  cammino_max = 0
  n_max = 1
  memoria = {}
   
  for n in xrange(1,1000000):
    cammino, memoria = collatz_con_memoria(n, n, 0, memoria)
    if(memoria[n] > cammino_max):
      cammino_max = memoria[n]
      n_max = n
  return n_max, cammino_max  
 
'''	
start = time.time()
n_max, cammino_max = very_brute()
end = time.time()
print "max: ", n_max, " - ", cammino_max
print "tempo: ", (end-start)

start = time.time()
n_max, cammino_max = better()
end = time.time()
print "max: ", n_max, " - ", cammino_max
print "tempo: ", (end-start)
'''

race = {
    'problemName': '14',
    'author': 'valeria',
    'raceables': { 
	    'very_brute': very_brute
        'better': better
    }
}

if __name__ == "__main__":
  print better()

