import python_scripts.correct_labels.data as data
import numpy as np
import pdb
from PIL import Image

dt = data.Data()

def keyToLabel(k):
    if (k=='Fondo'):
        label=0
    elif (k=='Cara'):
        label=1
    elif (k == 'CejaDerecha'):
        label = 2
    elif (k == 'CejaIzquierda'):
        label = 3
    elif (k == 'OjoDerecho'):
        label = 4
    elif (k == 'OjoIzquierdo'):
        label = 5
    elif (k == 'Nariz'):
        label = 6
    elif (k == 'LabioSuperior'):
        label = 7
    elif (k == 'InteriorBoca'):
        label = 8
    elif (k == 'LabioInferior'):
        label = 9
    elif (k == 'Pelo'):
        label = 10
    else:
        label = dt.noColor
    return label

def openFilename(str):
    return openAsArray(dt.source+str)

def openAsArray(str):
    return np.array(Image.open(str))

def saveAsArray(a,str):
    Image.fromarray(a).save(str)
    return

def deColour(label, img):
    #img = np.array(Image.open(source+row['filename']))
    #label = keyToLabel(k)
    for i in range(len(img)):
        for j in range(len(img[i])):
            if (img[i][j]==label):
                img[i][j]=dt.noColor

def reColourConj(v, img, label):
    v_x,v_y=int(v[0]),int(v[1])
    x,y = v_x,v_y
    #x,y=0,0
    #Buscamos en 4 direcciones el pixel más cercano al centroide,
    #aunque lo mas comun sera que el centroide este dentro
    for i in range(128):
        if (v_x + i < len(img) and img[v_x + i,v_y] == dt.noColor):
            x, y = v_x + i, v_y
            break
        elif (v_x - i > -1 and img[v_x - i,v_y] == dt.noColor):
            x, y = v_x - i, v_y
            break
        elif (v_y + i < len(img[v_x]) and img[v_x,v_y + i] == dt.noColor):
            x, y = v_x, v_y + i
            break
        elif (v_y - i > -1 and img[v_x,v_y - i] == dt.noColor):
            x, y = v_x, v_y - i
            break
    #print((x,y))

    pixelList = [(x,y)]
    img[x][y]=label
    #print(x,y)
    index = 0
    n = 1
    while index < len(pixelList):
        newPixels = pixelsArround(img, pixelList[index])
        #print(str(index) + ' , ' + str(newPixels))
        for (i,j) in newPixels:
            img[i,j]=label
            n+=1
            pixelList.append((i,j))
        index+=1

    if (n==v[2]):
        return True
    else:
        return n

def pixelsArround(a, pixel):
    res=[]
    x,y = pixel[0],pixel[1]
    for i in range(x-1,x+2):
        if (i==len(a)):
            continue
        for j in range(y-1,y+2):
            if (j==len(a[i])):
                continue
            if (i==x and j==y):
                continue
            if (a[i,j]==dt.noColor):
                res.append((i,j))
    return res

def reColourVoid(img):
    noColorpixels = searchNoColor(img)
    #print(noColorpixels)
    it = 0
    while len(noColorpixels)>0 and it<100:
        it+=1
        for (i,j) in noColorpixels:
            boolean, colour = newColour(img,(i,j))
            #pdb.set_trace()
            if boolean:
                img[i,j]=colour
                noColorpixels.remove((i,j))
        #print(len(noColorpixels))
    return img

def searchNoColor(img):
    noColorpixels = []
    for i in range(len(img)):
        for j in range(len(img[i])):
            if (img[i,j]==dt.noColor):
                noColorpixels.append((i,j))
    return noColorpixels

def newColour(img, pixel):
    (x,y) = pixel
    labelsCount = [0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(x-1,x+2):
        for j in range(y-1,y+2):
            if (i<0 or i==len(img) or j<0 or j==len(img[i])):
                continue
            elif (i==x and j==y):
                continue
            else:
                labelsCount[img[(i,j)]]+=1
    #pdb.set_trace()

    for t_label in range(2,10):
        if labelsCount[t_label]>2:
            return True, t_label
    if labelsCount[0]>3:
        return True, 0
    elif labelsCount[1]>2:
        return True, 1
    elif labelsCount[10]>2:
        return True, 10
    else:
        return False, dt.noColor


####################################################################################################
####################        Transformaciones del postanalisis                   ####################
####################                                                            ####################
####################################################################################################
####################################################################################################

def postNariz(a, vectores, label=6, min_count=24, min_len=700):
    boolean = True
    nariz = None
    if len(vectores)>1:
        x_min = 0
        for v in vectores:
            if v[2] > min_len:
                nariz = v
                boolean = False
            if int(v[0])>x_min:
                x_min = int(v[0])
                x,y =int(v[0]),int(v[1])
        for v in vectores:
            for x in range(int(v[0]), x_min):
                a[x,int(v[1])]=label
                a[x, int(v[1]+1)] = label
                a[x, int(v[1]-1)] = label
    else:
        if vectores[0][2]>min_len:
            nariz = vectores[0]
            boolean=False

    if boolean:
        perimetro = getPerimetro(a, label)
    else:
        x = int(nariz[0])
        max = countLine(a,x,label)
        while (max-countLine(a,x+1,label))<2:
            if max<countLine(a,x+1,label):
                max = countLine(a, x + 1, label)
            x=x+1
        for i in range(x+2, len(a)):
            for j in range(len(a[i])):
                if a[i,j]==label:
                    a[i,j]=dt.noColor


    #Rellenmos
    n=0
    while boolean:
        boolean = False
        newPixels = []
        for pixel in perimetro:
            #print(pixel)
            if labelArroundDim(a,pixel,label)>min_count:
                n += 1

                boolean = True
                newPixels.append(pixel)
                a[pixel[0],pixel[1]] = label
        #pdb.set_trace()
        for pixel in newPixels:
            perimetro.remove(pixel)
            (x,y)=pixel
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 2):
                    if (i == x and j == x) or (a [i,j]==label) or (perimetro.count((i,j)!=0)):
                        continue
                    elif isPeremeter(a,(i,j),label):
                        perimetro.append((i,j))
        #pdb.set_trace()
    #print('relleno : '+str(n))

def countLine(img, x, label):
    count = 0
    for j in range(len(img[x])):
        if img[x,j]==label:
            count+=1
    return count

def getPerimetro(img, label):
    perimetro = []
    no_perimetro = []
    x,y = findPixel(img, label)
    for i in range(x-1,x+2):
        for j in range(y-1,y+2):
            if img[i,j]==label:
                continue
            elif isPeremeter(img,(i,j), label):
                perimetro.append((i,j))
    index=0
    while index<len(perimetro):
        #print(str(index) + ' : ' + str(len(perimetro))+ ' : ' + str(len(no_perimetro)) )
        (x,y) =  perimetro[index]
        #pdb.set_trace()
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if (i==x and j ==y) or (img[x,y]==label) or (no_perimetro.count((i,j))!=0)or (perimetro.count((i,j))!=0):
                    continue
                if isPeremeter(img,(i,j), label):
                    perimetro.append((i,j))
                else:
                    no_perimetro.append((i,j))
        index+=1
    return perimetro

def labelArroundDim(a, pixel, label, dim = 3):
    count = 0
    x,y = pixel[0],pixel[1]
    for i in range(x-dim,x+dim+1):
        if (i==len(a)):
            continue
        for j in range(y-dim,y+dim+1):
            if (j==len(a[i])):
                continue
            if (i==x and j==y):
                continue
            if (a[i,j]==label):
                count+=1
    return count

def countLabelArround(a, pixel, label):
    res=[]
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

def findPixel(img, label):
    for i in range(len(img)):
        for j in range(len(img[i])):
            if img[i,j]==label:
                return i,j

def isPeremeter(img, pixel, label):
    (x,y)=pixel
    for i in range(x-1,x+2):
        for j in range(y-1,y+2):
            if (i==x and j ==x):
                continue
            if img[i,j]==label:
                return True
    return False

def postCeja(img ,vectores, key):
    label = keyToLabel(key)
    #pdb.set_trace()
    for v in vectores:
        v_x, v_y = int(v[0]), int(v[1])
        x, y = v_x, v_y
        # x,y=0,0
        # Buscamos en 4 direcciones el pixel más cercano al centroide,
        # aunque lo mas comun sera que el centroide este dentro

        for i in range(128):
            if (v_x + i < len(img) and img[v_x + i, v_y] == label):
                x, y = v_x + i, v_y
                break
            elif (v_x - i > -1 and img[v_x - i, v_y] == label):
                x, y = v_x - i, v_y
                break
            elif (v_y + i < len(img[v_x]) and img[v_x, v_y + i] == label):
                x, y = v_x, v_y + i
                break
            elif (v_y - i > -1 and img[v_x, v_y - i] == label):
                x, y = v_x, v_y - i
                break

        pixelList = [(x, y)]
        pintar = []
        index=0
        #pdb.set_trace()
        while index<len(pixelList):
            (x,y)=pixelList[index]
            for i in range(x-1,x+2):
                for j in range(y-1,y+2):
                    if img[i,j]==label and pixelList.count((i,j))==0:
                        pixelList.append((i,j))
            index+=1
        for (i,j) in pixelList:
            if img[i,j]==label and img[i,j+1]!=label and img[i-1,j+1]!=label:
                for j2 in range(j+1,len(img[i])):
                    if img[i,j2]==label:
                        for j3 in range(j+1,j2):
                            pintar.append((i,j3))
                        break
        #pdb.set_trace()
        for (i,j) in pintar:
            img[i,j]=label
        #print('relleno '+ str(len(pintar)))

def postOjo(img, vectores, key):
    label = keyToLabel(key)
    for v in vectores:
        v_x, v_y = int(v[0]), int(v[1])
        x, y = v_x, v_y
        for i in range(128):
            if (v_x + i < len(img) and img[v_x + i, v_y] == label):
                x, y = v_x + i, v_y
                break
            elif (v_x - i > -1 and img[v_x - i, v_y] == label):
                x, y = v_x - i, v_y
                break
            elif (v_y + i < len(img[v_x]) and img[v_x, v_y + i] == label):
                x, y = v_x, v_y + i
                break
            elif (v_y - i > -1 and img[v_x, v_y - i] == label):
                x, y = v_x, v_y - i
                break

        pixelList = [(x, y)]
        pintar = []
        index = 0
        # pdb.set_trace()
        while index < len(pixelList):
            (x, y) = pixelList[index]
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 2):
                    if img[i, j] == label and pixelList.count((i, j)) == 0:
                        pixelList.append((i, j))
            index += 1
        for (i, j) in pixelList:
            if img[i, j] == label and img[i, j + 1] != label:
                for j2 in range(j + 1, len(img[i])):
                    if img[i, j2] == label:
                        for j3 in range(j + 1, j2):
                            pintar.append((i, j3))
                        break
        for (i, j) in pixelList:
            if img[i, j] == label and img[i+1, j] != label:
                for i2 in range(i + 1, len(img)):
                    if img[i2, j] == label:
                        for i3 in range(i + 1, i2):
                            pintar.append((i3, j))
                        break
        for (i, j) in pintar:
            img[i, j] = label






