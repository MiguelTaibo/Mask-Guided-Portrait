
#Busca en la imagen (como array) el centroide del embedding  correspondiente a la label
    # a : in : np array : array de la mascara
    # label : in : int : etiqueta del embbeding que queremos buscar
    # x/n, y/n : out : double,double : centroide del embedding
    # n : out : int : numero de pìxeles del embedding
def searchEmb(a, label):
    x,y,n=0,0,0
    for i in range(len(a)):
        for j in range(len(a[0])):
            if (a[i,j]==label):
                x+=i
                y+=j
                n+=1
    if (n==0):
        return -1,-1,0
    else:
        return x/n,y/n,int(n)

#Busca en la imagen (como array) el centroide de un conjunto compacto
# del embedding  correspondiente a la label
    # a : in : np array : array de la mascara
    # label : in : int : etiqueta del intervalo compacto del  embbeding que queremos buscar
    # x/n, y/n : out : double,double : centroide intervalo compacto
    # n : out : int : numero de pìxeles del intervalo compacto
def searchCompact(a, label):
    for i in range(len(a)):
        time_break = False
        for j in range(len(a[0])):
            if (a[i,j]==label):
                x,y = int(i),int(j)
                time_break = True
                break
        if (time_break):
            break
    pixelList = [(x,y)]
    index = 0
    x,y,n=x,y,1
    while index < len(pixelList):
        newPixels = pixelsArround(a, pixelList[index], label)
        for e in newPixels:
            if (pixelList.count(e)==0):
                pixelList.append(e)
                x+=e[0]
                y+=e[1]
                n+=1
        index+=1
    if (n==0):
        return -1,-1,0
    else:
        return x/n,y/n,int(n)

#Comprueba si el embedding de una label es completamente compacto
def isCompact(a,label):
    if(searchCompact(a,label)==searchEmb(a, label)):
        return True
    else:
        return False

#Busca en la imagen (como array) los centroide de todos conjunto compacto
# del embedding  correspondiente a la label
    # a : in : np array : array de la mascara
    # label : in : int : etiqueta del intervalo compacto del  embbeding que queremos buscar
    # res : out : lista que contiene para cada un de los intervalos:
    #   x/n, y/n : double,double : centroide intervalo compacto
    #   n : int : numero de pìxeles del intervalo compacto
def searchCompactIntervals(a, label):
    res = []
    a_temp = a
    while True:
        x,y=-1,-1
        #Buscamos un pixel sobre el que encontramos to.do el intervalo compacto
        for i in range(len(a_temp)):
            time_break = False
            for j in range(len(a_temp[0])):
                if (a_temp[i,j]==label):
                    x,y = int(i),int(j)
                    time_break = True
                    break
            if (time_break):
                break
        #print(x,y)
        # Si no encontramos ningun pixel salimos
        if(x==-1 or y==-1):
            break

        #Para cada pixel del intervalo miramos si hay algun vecino pixel que no hayamos
        # añadido anteriormente al intervalo, empezando por el pixel del apartado anterior
        pixelList = [(x,y)]
        a_temp[x,y]=12
        index = 0
        n=1
        while index < len(pixelList):
            newPixels = pixelsArround(a, pixelList[index], label)
            for e in newPixels:
                if (pixelList.count(e)==0):
                    pixelList.append(e)
                    a_temp[e[0],e[1]]=12
                    x+=e[0]
                    y+=e[1]
                    n+=1
            index+=1
        res.append((x/n,y/n,int(n)))
    return res

def pixelsArround(a, pixel, label):
    res=[];
    x,y = pixel[0],pixel[1]
    for i in range(x-1,x+2):
        if (i==len(a)):
            continue
        for j in range(y-1,y+2):
            if (j==len(a[i])):
                continue
            if (i==x and j==y):
                continue
            if (a[i,j]==label):
                res.append((i,j))

    return res

def createLabelDiccionary(a):
    diccionario = {
        'Fondo'         : searchCompactIntervals(a, 0),
        'Cara'          : searchCompactIntervals(a, 1),
        'CejaDerecha'   : searchCompactIntervals(a, 2),
        'CejaIzquierda' : searchCompactIntervals(a, 3),
        'OjoDerecho'    : searchCompactIntervals(a, 4),
        'OjoIzquierdo'  : searchCompactIntervals(a, 5),
        'Nariz'         : searchCompactIntervals(a, 6),
        'LabioSuperior' : searchCompactIntervals(a, 7),
        'InteriorBoca'  : searchCompactIntervals(a, 8),
        'LabioInferior' : searchCompactIntervals(a, 9),
        'Pelo'          : searchCompactIntervals(a, 10),
    }
    return diccionario;