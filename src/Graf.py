import PriorityQueue
import math

"""
Class Graf: digunakan untuk merepresentasikan graf dari peta, dengan simpul berupa suatu koordinat pada peta dengan format NamaSimpul latitude longitude
-> Mempunyai atribut:
	- graf : matriks ketetanggaan berbobot dengan bobot berupa jarak antara simpul yang bertetangga
	- hn : metriks dengan elemen berupa jarak dari suatu simpul ke simpul lainnya, diolah oleh program
	- vertex : array of vertex yang terdapat pada graf
	- vertexidx: dictionary dengan key merupa namasimpul dan value berupa indeks pada matriks ketetanggaan yang relate dengan nama simpul
	- visited : dictionary of boolean untuk menyimpan informasi apakah suatu simpul telah dikunjungi atau belum
	- solutionPath: list of path yang merupakan shortest path dari simpul awal ke simpul goal
	- queue: priority queue dengan elemen merupakan list of path
-> Mempunyai method:
	- initializeQueue: Menginisialisasi objek priority queue, dipanggil pada method Astar untuk menginisialisasi queue awal
	- addVertex: Menambahkan vertex dengan indeks sesuai pada graf ketetanggaan
	- haversineFormula: Untuk menghitung jarak antar dua koordinat di peta
	- getHnMatriks: Method yang digunakan untuk membentuk atribut hn
	- addGraf: Menambahkan graf ketetanggaan dengan parameter matriks ketetanggaan dari inputfile (user harus menginput matriks ketetanggaannya sendiri)
	- buildGrafBool: Mengecek dan mengubah input dari graf jika input dari graf merupakan matriks adjacency boolean, jika telah dalam bentuk jarak tidak akan diubah
	- total_jarak: Menghitung total jarak dari suatu path (jarak dari simpul awal ke simpul n)
	- Astar: Algoritma untuk mencari shortest path
	- findShortestPath: Method yang dipanggil user untuk membentuk matriks hn (getHnMatriks), mencari jalur terdekat(Astar), dan menampilkan solusi(printSolusi)
	- getSolution: Mengembalikan list of path
	- isVertex: Mengecek apakah suatu input nama simpul merupakan simpul dalam graf
	- printSolusi: Mencetak solusi dalam bentuk text berupa path dan total jarak yang dilaluinya
	- clearGraf: Mengosongkan graf agar bisa digunakan berulangkali
-> CATATAN: Untuk mencari jalur terpendek gunakan langsung method findShortestPath, JANGAN memanggil algoritma Astar langsung
"""

class Graf:
	def __init__(self):
		self.graf = [] # Matriks ketetanggaan dengan bobot merupakan jarak antar simpul
		self.hn = [] # Matriks dengan elemen berupa jarak dari suatu simpul ke simpul lainnya
		self.vertex = [] # Array dari kumpulan simpul dengan format [namasimpul, [latitude, longitude]]
		self.vertexidx = {} # Dictionary untuk mendapatkan indeks simpul dengan key berupa namasimpul dan value integer
		self.visited = {} # Dictionary untuk mengecek apakah suatu simpul telah dikunjungi atau belum dengan key berupa namasimpul dan value boolean
		self.solutionPath = [] # Untuk menyimpan solusi, berupa list of path
		self.queue = [] # Queue untuk membantu penarian solusi dengan menggunakan algoritma A*

	# Inisialisasi queue sebagai objek PriorityQueue dengan maxEl jumlah simpul^2
	def initializeQueue(self):
		self.queue = PriorityQueue.PriorityQueue(len(self.vertex) ** 2)

	# Menambah simpul dengan format vertex adalah [namasimpul, [latitude, longitude]]
	# Menambahkan indeks pada matriks sesuai dengan urutan
	# Dipanggil ketika membaca input graf secara iteratif seingga indeksnya dapat ditentukan
	# Contoh terdapat 8 simpul maka indeks mulai dari 0 sampai 7
	def addVertex(self, vertex, idx):
		self.vertex += [vertex]
		self.vertexidx[vertex[0]] = idx

	# Mencari jarak antar dua koordinat
	def haversineFormula(self, Lat1, Long1, Lat2, Long2):
		dLat = ((Lat2-Lat1)*math.pi)/180
		dLong = ((Long2-Long1)*math.pi)/180
		a = ((math.sin(dLat/2)) ** 2) + math.cos(Lat1 * math.pi/180) * math.cos(Lat2 * math.pi /180) * ((math.sin(dLong/2)) ** 2)
		c = 2 * math.asin(math.sqrt(a))
		return 6371000 * c

	# Membuat matriks hn dimana isinya merupakan jarak dari suatu simpul ke simpul lainnya
	def getHnMatrix(self):
		self.hn = [[0 for j in range(len(self.vertex))] for i in range(len(self.vertex))]
		for vertex1 in self.vertex:
			for vertex2 in self.vertex:
				if(vertex1[0] == vertex2[0]):
					self.hn[self.vertexidx[vertex1[0]]][self.vertexidx[vertex2[0]]] = 0
				else:
					self.hn[self.vertexidx[vertex1[0]]][self.vertexidx[vertex2[0]]] = self.haversineFormula(vertex1[1][0], vertex1[1][1], vertex2[1][0], vertex2[1][1])

	# Menambahkan representasi graf adjacency matriks yang telah diolah dari input file
	def addGraf(self, graf):
		self.graf = graf	

	
	# Method untuk menghitung jarak total dari current path, dari simpul awal ke simpul n
	def total_jarak(self, path):
		if(len(path) <= 1):
			return 0
		else:
			total = 0
			for i in range(len(path)-1):
				total += self.graf[self.vertexidx[path[i][0]]][self.vertexidx[path[i+1][0]]]
			return total

	# Algoritma A* untuk mencari jalur terpendek
	# Secara umum algoritmanya seperti BFS namun queue yang digunakan adalah Priority Queue yang sudah disesuaikan
	def Astar(self, Vfirst, Vgoal):
		self.initializeQueue() # Inisialisasi queue
		self.queue.push([self.vertex[self.vertexidx[Vfirst]]+[0]]) # add list of vertex ke queue dengan format [namasimpul, [latitude, longitude], f(n)]
		for i in self.vertex:
			self.visited[i[0]] = False # Inisialisasi semua simpul belum dikunjungi
		while(self.queue.getNeff()>0): # Ketika queue belum kosong
			path = self.queue.pop() # pop queue untuk mendapatkan path yang akan diperiksa
			total_jarak = self.total_jarak(path) # Total jarak dari simpul awal ke simpul yang sedang diperiksa
			Vcurr = path[-1] # Mendapatkan simpul yang akan diperiksa dengan format [namasimpul, [latitude, longitude], f(n)]
			self.visited[Vcurr[0]] = True # Tandai Vcurr telah dikunjungi
			if (Vcurr[0] == Vgoal): # Jika simpul solusi diperiksa maka masukkan kedalam solution path dan pencarian dihentikan
				self.solutionPath.append(path)
				return
			# Tambahkan simpul yang bertetangga ke queue
			for adjacent in range(len(self.graf[self.vertexidx[Vcurr[0]]])):
				# Jika bobot Vcurr dan adjacent tidak sama dengan 0 serta simpul yang bertetangga belum dikunjungi
				if (self.graf[self.vertexidx[Vcurr[0]]][adjacent] != 0 and self.visited[self.vertex[adjacent][0]] == False):
					# Tambahkan kedalam queue
					newPath = list(path)
					newPath.append(self.vertex[adjacent] + [total_jarak + self.graf[self.vertexidx[Vcurr[0]]][adjacent] + self.hn[adjacent][self.vertexidx[Vgoal]]])
					self.queue.push(newPath)

	# Untuk mencari jalur terpendek, user harus memanggil method ini
	def findShortestPath(self, Vfirst, Vgoal):
		self.buildGrafBool()
		self.getHnMatrix()
		self.solutionPath = []
		self.Astar(Vfirst, Vgoal)
		self.printSolusi()

	# Method untuk mendapatkan solusi
	def getSolution(self):
		return self.solutionPath

	# Method untuk mengecek suatu input string merupakan simpul dari graf atau bukan
	def isVertex(self, vertex):
		for v in self.vertex:
			if(v[0] == vertex):
				return True
		return False

	# Untuk menampilkan shortest path yang berbentuk text
	def printSolusi(self):
		if(len(self.solutionPath) == 0):
			print("Tidak ada solusi")
		else:
			strPrint = ""
			for vertex in self.solutionPath[0]:
				strPrint += vertex[0]
				if(vertex[0] != self.solutionPath[0][len(self.solutionPath[0])-1][0]):
					strPrint += " -> "
				else:
					strPrint += "\nDengan total jarak adalah " + str(vertex[2])
			print(strPrint)

	# Mengosongkan graf
	def clearGraf(self):
		self.graf = []
		self.hn = []
		self.vertex = []
		self.vertexidx = {}

	# Mengecek dan mengubah graf yang berupa matriks adjacency boolean
	# Jika input bobot antar simpul telah dalam bentuk jarak maka tidak akan diubah
	def buildGrafBool(self):
		cekGraf = {}
		for i in self.graf:
			for j in i:
				cekGraf[j] = j
		for key in cekGraf:
			if(key != 0 and key != 1):
				return
		for vertex1 in self.vertex:
			for vertex2 in self.vertex:
				if(self.graf[self.vertexidx[vertex1[0]]][self.vertexidx[vertex2[0]]] == 0):
					self.graf[self.vertexidx[vertex1[0]]][self.vertexidx[vertex2[0]]] = 0
				else:
					self.graf[self.vertexidx[vertex1[0]]][self.vertexidx[vertex2[0]]] = self.haversineFormula(vertex1[1][0], vertex1[1][1], vertex2[1][0], vertex2[1][1])