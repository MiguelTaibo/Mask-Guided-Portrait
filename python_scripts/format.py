#! /usr/bin/python
from argparse import ArgumentParser
import sys, os, shutil
import numpy as np
from PIL import Image

parser = ArgumentParser(description='%(prog)s is an ArgumentParser demo')

parser.add_argument('-s',                       help='imagen que se transformará')
parser.add_argument('-f', default='',           help='dirección destino')
parser.add_argument('-n', default='0',          help='disminucion tamano')
parser.add_argument('-nl', default='0',         help='disminucion tamano izquierda')
parser.add_argument('-nr', default='0',         help='disminucion tamano derecha')
parser.add_argument('-nu', default='0',         help='disminucion tamano arriba')
parser.add_argument('-nd', default='0',         help='disminucion tamano abajo')
parser.add_argument('-r', default='False',      help='Para borrar la foto original', action='store_true')
parser.add_argument('-m', default='False',      help='Para mostrar la imagen', action='store_true')
parser.add_argument('-p', default='False',      help='Preparar par al hace test_netP crear las mascaras', action='store_true')
parser.add_argument('-t', default='0',          help='angulo a transponer')

args = parser.parse_args()
sourceAddr=args.s
destinyAdd=args.f

nArg = int(args.n) * 256
nl = int(args.nl) * 128
nr = int(args.nr) * 128
nu = int(args.nu) * 128
nd = int(args.nd) * 128
tArg = int(args.t)

if (destinyAdd==''):
    n = sourceAddr.find('.')
    destinyAdd = sourceAddr[0:n]+'.png'

img = Image.open(sourceAddr).convert('RGB')
a = np.array(img)

x, y, n = len(a[0]), len(a), 0
while(x>256 and y>256):
   n+=256
   x-=256
   y-=256

y_i, y_f, x_i, x_f = int((y+nArg)/2+nu),int((y-nArg)/2+n+nd),int((x+nArg)/2+nl),int((x-nArg)/2+n+nd)
b=(a[y_i:y_f,x_i:x_f,:]).transpose(1,0,2)
b=a[y_i:y_f,x_i:x_f,:]

img2 = Image.fromarray(b)
img2 = img2.rotate(tArg).resize((256,256))

img2.save(destinyAdd)
print ('Guardamos la foto '+ destinyAdd)
if (args.r == True):
    os.remove(sourceAddr)
    print('Borramos la foto '+ sourceAddr)
if (args.m==True):
    img2.show()

if(args.p==True):
    n1=destinyAdd.find('_img')
    shutil.copy(destinyAdd[0:n1]+'_label/173.png',
                destinyAdd[0:n1]+'_label/'+destinyAdd[n1+5:len(destinyAdd)])
    img2.save(destinyAdd[0:n1]+'2'+destinyAdd[n1:len(destinyAdd)])

    print('Generamos la mascara falsa '+ destinyAdd[0:n1]+'_label/'+destinyAdd[n1+5:len(destinyAdd)])
    print(destinyAdd[0:n1]+'2'+destinyAdd[n1:len(destinyAdd)])
exit()