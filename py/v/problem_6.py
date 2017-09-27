def solve():

	somma_doppi_prodotti = 0
	for i in range(1,101):
		for j in range(i+1,101):
			somma_doppi_prodotti += 2*i*j
	return somma_doppi_prodotti
	
	
race = {
	'author': 'valeria',
	'problemName': '6',
	'raceables': { 
		'blocchetto': solve
	}  
}

if __name__ == "__main__":
    print solve()
