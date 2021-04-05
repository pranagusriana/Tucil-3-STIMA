"""
Class PriorityQueue: digunakan sebagai queue di class graf untuk membantu pencarian lintasan terpendek dengan menggunakan algoritma A*
-> Mempunyai atribut:
    - queue: array berukuran maxEl untuk menyimpan elemen queue yang berupa list of [namaSimpul, [latitude, longitude], fn] (lintasan)
    - neff: jumlah elemen yang telah tersimpan pada queue
    - MaxEl : Max element dari queue
-> Mempunyai method:
    - __init__ : konstruktor class PriorityQueue user defined maxEl
    - push : untuk menambahkan element pada queue sesuai dengan nilai fn
    - pop : menghapus elemen paling awal lalu mengembalikan nilai elemen paling awal tersebut
    - getNeff : mendapatkan neff
    - getQueue : mendapatkan queue
    - getMaxEl : mendapatkan maxEl
    - printPriorityQueue: untuk menampilkan neff, maxEL, dan seluruh elemen queue
"""

class PriorityQueue:
    def __init__(self, maxEl):
        self.queue = [0 for i in range(maxEl)]
        self.neff = 0
        self.maxEl = maxEl

    def push(self, element):
        idx = self.neff
        while(idx > 0):
            if(element[len(element)-1][2] < self.queue[idx-1][len(self.queue[idx-1])-1][2]):
                self.queue[idx] = self.queue[idx-1]
                idx -= 1
            else:
                break
        self.queue[idx] = element
        self.neff += 1

    def pop(self):
        temp = self.queue[0]
        for i in range(self.neff-1):
            self.queue[i] = self.queue[i+1]
        self.neff -= 1
        return temp

    def getNeff(self):
        return self.neff

    def getQueue(self):
        return self.queue

    def getMaxEl(self):
        return self.maxEl

    def printPriorityQueue(self):
        print("Neff:", self.neff)
        print("MaxEL:", self.maxEl)
        for i in range(self.neff):
            print(self.queue[i])