# Untuk membaca file input yang terdapat di folder test
def readInputFromFile(namaFile, arrayv, graf):
    file = open("../test/"+namaFile, "r")
    file_input = file.readlines()
    nvertex = int(file_input[0])
    graftemp = [[0 for j in range(nvertex)] for i in range(nvertex)]
    i = 1
    while(i < nvertex+1):
        j = 0
        nama_simpul = ""
        koordinat = []
        tempstr = file_input[i].split()
        while (j < len(tempstr)):
            if(j==0):
                nama_simpul += tempstr[j]
            else:
                koordinat += [float(tempstr[j])]
            j += 1
        arrayv += [[nama_simpul, koordinat]]
        i += 1
    while(i < 2*nvertex+1):
        tempstr = file_input[i].split()
        for j in range(len(tempstr)):
            graftemp[i-nvertex-1][j] = float(tempstr[j])
        i += 1
    file.close()
    graf += graftemp