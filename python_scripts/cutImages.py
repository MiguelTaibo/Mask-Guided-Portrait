#! /usr/bin/python
from argparse import ArgumentParser
import glob, os
from PIL import Image
import numpy as np

def recortar(a):

    y_i, y_f, x_i, x_f = int(y), int(y+f), int(x), int(x+f)
    return a[y_i:y_f,x_i:x_f,:]

parser = ArgumentParser(description='%(prog)s is an ArgumentParser demo')

parser.add_argument('-s',                       help='carpeta que se transformará')
parser.add_argument('-x', default='0',          help='disminucion tamano izquierda')
parser.add_argument('-y', default='0',          help='disminucion tamano derecha')
parser.add_argument('-n', default='1',          help='factor entero')
parser.add_argument('-m', default='False',      help='Para mostrar la imagen y ser de prueba', action='store_true')
parser.add_argument('-l', default='False',      help='Para copiar las labels', action='store_true')

args = parser.parse_args()
sourceAddr=args.s
x = int(args.x)
y = int(args.y)
f = int(float(args.n) * 256)

for filename in glob.glob(sourceAddr+'*.png'):
    img = Image.fromarray(recortar(np.array(Image.open(filename)))).resize((256,256))
    if (args.m ==True):
        img.show()
        print(Image.open(filename).getbbox())
        break
    else:
        img.save(filename)