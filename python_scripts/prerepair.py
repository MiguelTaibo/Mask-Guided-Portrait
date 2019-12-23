#! /usr/bin/python

from argparse import ArgumentParser
import sys, os, shutil
import numpy as np
from PIL import Image

#Array de transformacion: el indice es el valor de source y el valor es el color en el destino
colores =  np.array([
    [0,0,0,255],        # Fondo, negro
    [100,100,100,255],  # Cara, gris
    [255,255,0,255],    # Ceja derecha, amarilla
    [0,100,0,255],      # Ceja izquierda, verde oscuro
    [0, 255 ,255,255],  # Ojo  derecho, azul claro
    [0,0,100,255],      # Ojo izquierdo, azul oscuro
    [255,0,255,255],    # Nariz, violeta
    [255,0,0,255],      # Labio superior, rojo claro
    [0,0,255,255],      # Interior boca, Azul
    [0,255,0,255],      # Labio inferior, verde claro
    [255,255,255,255],  # pelo, blanco
])

parser = ArgumentParser(description='%(prog)s is an ArgumentParser demo')

parser.add_argument('-s', help='imagen que se arreglara')
args = parser.parse_args()
sourceAddr = args.s


def calcLabel (pixel):
    for i in range(len(colores)):
        if (pixel==colores[i]).all():
            return i

    return -1

def calcLabels(a):
    labels = np.zeros((len(a), len(a[0])))
    for i in range(len(a)):
        for j in range(len(a[i])):
            labels[i][j] = calcLabel(a[i][j])
    return labels.astype(int);

def correctPixel(i, j, labels):
    if (i == 0 or j == 0 or i == len(a) or j == len(a[0])):
        label = -1
        corrected = False
    else:
        labelsInt = labels[i - 1:i + 2, j - 1:j + 2]
        coloresInt = np.zeros(len(colores)).astype(int)

        for index, x in np.ndenumerate(labelsInt):
            if (index[0] == 1 or index[1] == 1):
                coloresInt[x] += 2
            else:
                coloresInt[x] += 1


        if (np.sum(coloresInt) > 2*coloresInt[int(labels[i][j])]):
            max = 0
            label = 0
            for x in range(len(coloresInt)):
                if (coloresInt[int(x)] > max):
                    max = coloresInt[int(x)]
                    label = x

            if (max > coloresInt[int(labels[i][j])] and label > 1):
                corrected = True
            else:
                corrected = False

        else:
            label = labels[i][j]
            corrected = False

    return label, corrected

img = Image.open(sourceAddr)
a = np.array(img)
nt=0
ni=0
n=1

labels= calcLabels(a)
lPixels = []

for i in range(len(a)):
    for j in range(len(a[i])):
        label, corrected = correctPixel(i, j, labels)
        if (corrected):
            n += 1;
            a[i][j] = colores[label]
            labels[i][j] = label
            lPixels.append([i,j])

print('it:' + str(ni)+ ' corregimos:'+ str(len(lPixels)))

while len(lPixels)!=0:

    lPixels_next=[]
    for x in lPixels:
        for i in range(x[0]-1,x[0]+2):
            for j in range(x[1]-1,x[1]+2):
                label, corrected = correctPixel(i, j, labels)
                if (corrected):
                    n += 1;
                    a[i][j] = colores[label]
                    labels[i][j] = label
                    lPixels_next.append([i, j])

    lPixels=lPixels_next
    print('it:' + str(ni) + ' corregimos:' + str(len(lPixels)))



print(str(nt)+ ' bits corregidos')
print('en '+ str(ni)+ ' iteraciones')

img = Image.fromarray(a)
print('Guardamos'+ sourceAddr)
img.save(sourceAddr)
img.show()