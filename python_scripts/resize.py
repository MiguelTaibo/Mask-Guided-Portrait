#! /usr/bin/python

from argparse import ArgumentParser
import sys, os, shutil
import numpy as np
from PIL import Image
import skimage.measure

parser = ArgumentParser(description='%(prog)s is an ArgumentParser demo')
parser.add_argument('-s', help='carpeta con imagenes')
parser.add_argument('-g', default='False', help='si guardar', action='store_true')
parser.add_argument('-l', default='False', help='si label', action='store_true')
args = parser.parse_args()
sourceAddr = args.s
print (args.l)
for item in os.listdir(sourceAddr):
    img = Image.open(sourceAddr + item)
    # Aplicamos un maxpoolin
    if (args.l == True):
        a = skimage.measure.block_reduce(np.array(img), (2, 2), np.max)
    else:
        a = skimage.measure.block_reduce(np.array(img), (2, 2, 1), np.max)
    print(sourceAddr + item + '  ' + str(np.array(img).shape) + '->' + str(a.shape))
    img = Image.fromarray(a)
    if (args.g == True):
        img.save(sourceAddr + item)
