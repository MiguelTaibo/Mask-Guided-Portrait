import shutil, os
import glob
from argparse import ArgumentParser



parser = ArgumentParser(description='%(prog)s is an ArgumentParser demo')

parser.add_argument('-s',                       help='carpeta que se transformará')
parser.add_argument('-n', default='', 			help='nombre del video')
args = parser.parse_args()
sourceAddr=args.s
name = args.n

if (args.n==''):
	name = 'video'

try:
    os.stat(sourceAddr + name)
except:
    print('creamos directorio')
    os.mkdir(sourceAddr + name)

for filename in glob.glob(sourceAddr+'images/*_reconstruct_content_image.png'):
	
	n = filename.find('_reconstruct_content_image.png')
	if(n!=-1):
		n2=filename.find('/edit_latest/')
		destinyName = filename[0:n2]+'/edit_latest/'+name+'/'+filename[n2+20:n]+'.png'
		print(destinyName)
		shutil.copy(filename, destinyName)
