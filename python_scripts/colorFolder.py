#! /usr/bin/python

from argparse import ArgumentParser
import sys, os, shutil
import glob
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


#Array de transformacion: el indice es el valor de source y el valor es el color en el destino
colores =  [
    [0,0,0,255],        # 0: Fondo, negro
    [100,100,100,255],  # 1: Cara, gris
    [255,255,0,255],    # 2: Ceja derecha, amarilla
    [0,100,0,255],      # 3: Ceja izquierda, verde oscuro
    [0, 255 ,255,255],  # 4: Ojo  derecho, azul claro
    [0,0,100,255],      # 5: Ojo izquierdo, azul oscuro
    [255,0,255,255],    # 6: Nariz, violeta
    [255,0,0,255],      # 7: Labio superior, rojo claro
    [0,0,255,255],      # 8: Interior boca, Azul
    [0,255,0,255],      # 9: Labio inferior, verde claro
    [255,255,255,255],  # 10: Pelo, blanco
]

parser = ArgumentParser(description='%(prog)s is an ArgumentParser demo')

parser.add_argument('-s', help='imagen que se transformará')
parser.add_argument('-f', help='dirección destino', default='')

#Cargamos los parametros
args = parser.parse_args()
sourceAddr = args.s
destinyAddr = args.f

if (destinyAddr==''):
    n=sourceAddr.rfind('/')
    destinyAddr=sourceAddr[0:n]+'_t/';
    try:
        os.stat(destinyAddr)
    except:
        print('creamos directorio '+ destinyAddr)
        os.mkdir(destinyAddr)

for filename in sorted(glob.glob(sourceAddr+'*.png')):
    img = Image.open(filename).convert('RGBA')
    a = np.array(img)
    b = a
    # Modificamos la imagen
    for j in range(len(a[0, :, 0])):
        for k in range(len(a[:, j, 0])):
            b[k, j, :] = colores[a[k, j, 0]]
    img2 = Image.fromarray(b, 'RGBA')
    # Guardamos la imagen
    # img2.show()
    n=filename.rfind('/')
    print(destinyAddr+filename[n+1:len(filename)])
    img2.save(destinyAddr+filename[n+1:len(filename)])