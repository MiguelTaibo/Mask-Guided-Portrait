import python_scripts.correct_labels.analise as static
import python_scripts.correct_labels.timeAnalisie as dinamic
import python_scripts.correct_labels.remake as rmk
import python_scripts.correct_labels.remakeEye as re
import python_scripts.correct_labels.data as data
import glob
import csv
from PIL import Image
import numpy as np
import os

dt = data.Data()
source = dt.source
csv_columns = dt.csv_columns
name = dt.name

#tarda mucho
def diccionarysToCsv(str):
    with open(source+str+'.csv', mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
        writer.writeheader()
        dic = []
        for filename in sorted(glob.glob(source+'*.png')):
            a = np.array(Image.open(filename))
            dic_row = {'filename' :  filename[filename.rfind('/') + 1:len(filename)]}
            dic_row.update(static.createLabelDiccionary(a))
            dic.append(dic_row)
            print(filename)
        for data in dic:
            writer.writerow(data)

def filterLabels(etapa):
    if etapa=='preanalisis':
        analisis = dt.pre_analisis
    elif etapa == 'analisis':
        analisis = dt.analisis

    with open(source + analisis + '.csv', mode='r') as csv_file:
        print(source + analisis + '.csv')
        with open(source + name + '.csv', mode='w') as csv_wr:
            print(source + name + '.csv')
            reader = csv.DictReader(csv_file, fieldnames=csv_columns)
            writer = csv.DictWriter(csv_wr,fieldnames=csv_columns)
            writer.writeheader()
            #boolean = True
            buffer = [None, None, None]
            First = True
            for row in reader:
                if First:
                    First=False
                    continue
                row_mod, buffer = dinamic.correctProblems(row, buffer, etapa)
                #debug
                #print('De la imagen ' + str(row['filename']) +
                #      ' corregimos un problema en ' + str(k) +
                #      ' eligiendo ' +  str(v))
                #print(' entre ' + str(row[k]))
                #print(row_mod)
                writer.writerow(row_mod)
                # elif (k!=None and row != None):
                #     print('No hay prediccion espacio temporal posible para')
                #     print(k, str(row['filename']))

def preColour():
    with open(source + name + '.csv', mode='r') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=csv_columns)
        First=True
        for row in reader:
            if First:
                First=False
                continue
            print(row['filename'])
            try:
                a = rmk.openAsArray(source+row['filename'])
                re.reColourEyes(row,a)
                re.reColourMouth(row,a)
                rmk.saveAsArray(a, source + row['filename'])
            except:
                print('ERRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRROR')
                continue

def reColour(key):
    with open(source + name + '.csv', mode='r') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=csv_columns)
        First=True
        for row in reader:
            if First:
                First=False
                continue
            print(row['filename'] + ' : ' + row[key])
            try:
                a = rmk.openAsArray(source+row['filename'])
                vectores = dinamic.strToTupleList(row[key])
                label = rmk.keyToLabel(key)
                #print(label)
                rmk.deColour(label,a)
                for v in vectores:
                    rmk.reColourConj(v,a,label)
                postAnalisis(key, a, vectores)
                rmk.reColourVoid(a)
                rmk.saveAsArray(a, source+row['filename'])
            except:
                print('ERRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRROR')
                continue

def reColourKeys(keys):
    for key in keys:
        print('RECOLOUR: ' + key)
        reColour(key)
    print('Ejecutamos la transformacion de las mascaras para su visualizacion')
    os.system('python python_scripts/colorFolder.py -s datasets/exp2/aExp/')

def reColourAll():
    for key in dt.corrected_columns:
        print('RECOLOUR: ' + key)
        reColour(key)
    #print('Ejecutamos la transformacion de las mascaras para su visualizacion')
    #os.system('python python_scripts/colorFolder.py -s datasets/exp2/aExp/')

######## Tecnica de post analisis
def postAnalisis(key, a, vectores):
    if key=='Nariz':
        rmk.postNariz(a, vectores)
    elif key=='CejaDerecha' or key=='CejaIzquierda':
        rmk.postCeja(a,vectores, key)
    elif key=='ojoDerecho' or key=='OjoIzquierdo':
        rmk.postOjo(a,vectores,key)
    return

############ Funciones auxiliares
def printKey(key):
    with open(source + name + '.csv', mode='r') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=csv_columns)
        for row in reader:
            print(row['filename']+' : '+ row[key])

def searchInFile(str, temp):
    with open(source + temp + '.csv', mode='r') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=csv_columns)
        for row in reader:
            #print(row['filename'])
            if row['filename']==str:
                print(row)
                break
    return row

def postColour():
    with open(source + name + '.csv', mode='r') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=csv_columns)
        First=True
        for row in reader:
            if First:
                First=False
                continue
            print(row['filename'])
            try:
                a = rmk.openAsArray(source+row['filename'])
                re.reColourCara(row,a)
                rmk.saveAsArray(a, source + row['filename'])
            except:
                print('ERRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRROR')
                continue


