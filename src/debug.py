import PriorityQueue
import Graf
import FileProcessing
import math
import os

graf_peta = Graf.Graf()

array_of_vertex = []
adjacency_matriks_graf = []
N = input("Masukkan nama file: ")
while (not(os.path.isfile("../test/"+N))):
    print("File tidak ditemukan silahkan masukkan kembali input nama file,")
    N = input("Masukkan nama file: ")
FileProcessing.readInputFromFile(N, array_of_vertex, adjacency_matriks_graf)

idx = 0
graf_peta.clearGraf()
for vertex in array_of_vertex:
    graf_peta.addVertex(vertex, idx)
    idx += 1
graf_peta.addGraf(adjacency_matriks_graf)

simpul_awal = str(input("Masukkan simpul awal: "))
while(not(graf_peta.isVertex(simpul_awal))):
    print("Tidak terdapat simpul " + simpul_awal + ", silahkan masukkan kembali input simpul awal")
    simpul_awal = str(input("Masukkan simpul awal: "))
simpul_goal = str(input("Masukkan simpul tujuan: "))
while(not(graf_peta.isVertex(simpul_goal))):
    print("Tidak terdapat simpul " + simpul_goal + ", silahkan masukkan kembali input simpul tujuan")
    simpul_goal = str(input("Masukkan simpul tujuan: "))
graf_peta.findShortestPath(simpul_awal, simpul_goal)