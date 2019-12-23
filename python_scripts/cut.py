#! /usr/bin/python
from argparse import ArgumentParser
import sys, os, shutil
import glob
import numpy as np
from PIL import Image

def recortar(a):

    y_i, y_f, x_i, x_f = int(y), int(y+f), int(x), int(x+f)
    return a[y_i:y_f,x_i:x_f,:]

parser = ArgumentParser(description='%(prog)s is an ArgumentParser demo')

parser.add_argument('-s',                       help='carpeta que se transformará')
parser.add_argument('-f', default='',           help='carpeta destino')
parser.add_argument('-x', default='0',          help='disminucion tamano izquierda')
parser.add_argument('-y', default='0',          help='disminucion tamano derecha')
parser.add_argument('-n', default='1',          help='factor entero')
parser.add_argument('-r', default='False',      help='Para borrar la foto original', action='store_true')
parser.add_argument('-m', default='False',      help='Para mostrar la imagen y ser de prueba', action='store_true')
parser.add_argument('-p', default='False',      help='Preparar par al hace test_netP crear las mascaras', action='store_true')
parser.add_argument('-l', default='False',      help='Para copiar las labels', action='store_true')

args = parser.parse_args()
sourceAddr=args.s
destinyAdd=args.f
x = int(args.x)
y = int(args.y)
f = int(float(args.n) * 256)


label = ''
for filename in glob.glob(sourceAddr+'edit_label/*.png'):
    label = filename
    break;



if (destinyAdd==''):
   destinyAdd = sourceAddr

for filename in glob.glob(sourceAddr+'*.png'):
    img = Image.open(filename)
    #print(np.array(img).shape)
    img = Image.fromarray(recortar(np.array(img))).resize((256,256))
    if(args.m == True):
        img.show()
        break
    elif(args.r ==True):
        os.remove(filename)
    else:
        n = filename.find('.png')
        destinyName = filename[0:n-4]+'/edit_img/'+filename[n-3:n]+'.png'
        print(destinyName)
        img.save(destinyName)
        if (args.l==True):
            shutil.copy(label, destinyName)
    
   

