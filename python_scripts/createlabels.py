#! /usr/bin/python
from argparse import ArgumentParser
import shutil, os
import glob


parser = ArgumentParser(description='%(prog)s is an ArgumentParser demo')
parser.add_argument('-s',                       help='carpeta que se transformará')
args = parser.parse_args()
sourceAddr=args.s


print(sourceAddr+"edit_label/")
for filename in glob.glob(sourceAddr + "edit_label/*.png"):
    label=str(filename)

remove = True
temp = 0
for filename in glob.glob(sourceAddr + "/edit_img/*.png"):
    n = filename.find('.png')
    
    destinyName = sourceAddr + 'edit_label/'+filename[n-5:n]+'.png'
    print(destinyName)
    
    if (label!=destinyName):
    	shutil.copy(label,destinyName)    	
    else:
        remove = False
    
    temp+=1
    destinyName = sourceAddr + 'edit2_label/remove'+str(temp)+'.png'
    shutil.copy(label,destinyName)

    destinyName = sourceAddr + 'edit2_img/' +filename[n-4:n]+'.png'
    shutil.copy(filename,destinyName)


if(remove):
	os.remove(label)