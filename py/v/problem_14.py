import time

def collatz(n, cammino) :
  if (n == 1):
    return cammino
  if(n % 2 == 0):
    cammino += 1
    return collatz(n / 2, cammino)
  else:
    cammino += 2
    return collatz((3 * n + 1) / 2, cammino)
	
	
def collatz_con_memoria(N, n, cammino, memoria):
  if (n == 1):
    memoria[N] = cammino
    return cammino
  if( n < N ):
    return (memoria[n] + cammino)
  if(n % 2 == 0):
    cammino += 1
    return collatz_con_memoria(N, n / 2, cammino, memoria)
  else:
    cammino += 2
    return collatz_con_memoria(N, (3 * n + 1) / 2, cammino, memoria)
	
	
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
    cammino = collatz_con_memoria(n, n, 0, memoria)
    if(cammino > cammino_max):
      cammino_max = cammino
      n_max = n
  return n_max, cammino_max  
 
'''	
start = time.time()
n_max, cammino_max = very_brute()
end = time.time()
print "max: ", n_max, " - ", cammino_max
print "tempo: ", (end-start)
'''

start = time.time()
n_max, cammino_max = better()
end = time.time()
print "max: ", n_max, " - ", cammino_max
print "tempo: ", (end-start)

