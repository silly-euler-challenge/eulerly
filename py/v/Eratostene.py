import math

def Eratostene(N):

	setaccio = range(2,N)
	print (int)(math.sqrt(N))
	
	for i in range(2,(int)(math.sqrt(N))+1):
		print "i: ", i
		setaccio = list(filter((lambda x: (x%i!=0 or x==i)), setaccio))			
		
Eratostene(100)