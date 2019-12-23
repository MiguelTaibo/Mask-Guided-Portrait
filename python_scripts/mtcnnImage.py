from mtcnn import MTCNN
from PIL import Image
import numpy as np
import cv2
import glob
import csv
import math

csv_columns = ['filename', 'box', 'confidence', 'keypoints']
blanco = [255,255,255]
source = 'datasets/Miguel/'


def getCsv():
    with open(source + 'Miguel.csv', mode='w') as csv_file:
        #Take data
        detector = MTCNN()
        dic = []

        for filename in sorted(glob.glob(source+ '*.png')):
            img = cv2.imread(filename)
            try:
                dic_row = {'filename': filename[filename.rfind('/') + 1:len(filename)]}
                dic_row.update(detector.detect_faces(img)[0])
                dic.append(dic_row)
                print(filename)
            except:
                print(detector.detect_faces(img))
        #Write data on csv file
        writer = csv.DictWriter(csv_file, fieldnames = csv_columns)
        writer.writeheader()
        for data in dic:
            writer.writerow(data)

def printBox(row, a):
    box = row['box'][1:len(row['box']) - 1].split(',')
    [y, x, h, w] = [int(i) for i in box]
    for i in range(x, x + w):
        a[i, y] = blanco
        a[i, y + h] = blanco
    for i in range(y, y + h):
        a[x, i] = blanco
        a[x + w, i] = blanco
    a[x+w,y+h] = blanco
    return a

def printKeypoint(row, a):
    [(y_l_e, x_l_e), (y_r_e, x_r_e), (y_n, x_n), (y_m_l, x_m_l), (y_m_r, x_m_r)] = \
        eval(row['keypoints']).values()
    a[x_l_e, y_l_e] = blanco
    a[x_r_e, y_r_e] = blanco
    a[x_n, y_n] = blanco
    a[x_m_l, y_m_l] = blanco
    a[x_m_r, y_m_r] = blanco
    return a

def seePhotoWithKeypoints(row, s):
    with open(source + 'Cris.csv', mode='r') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=csv_columns)
        for row in reader:
            try:
                # print(row)
                if (s in row["filename"]):
                    img = Image.open(source + row['filename'])
                    a = np.array(img)
                    a = printBox(row, a)
                    a = printKeypoint(row, a)

                    img = Image.fromarray(a)
                    img.show()
                    break
            except:
                continue

def makePhoto(source, row):
    img = Image.open(source+ row['filename'])
    a = np.array(img)
    square = getBox(row)
    square = checkBorder(a, square)
    [x_i, x_f, y_i, y_f] = square
    print(square)
    img = Image.fromarray(a[x_i:x_f,y_i:y_f]).resize((256,256))
    return img

def getBox(row):
    box = row['box'][1:len(row['box']) - 1].split(',')
    [y_b, x_b, h, w] = [int(i) for i in box]
    y_c, x_c, n = int(y_b + h / 2), int(x_b + w / 2), int(math.ceil(1.3 * max([h, w]) / 256.0))
    [y_i, y_f, x_i, x_f] = [int(y_c - n * 128), int(y_c + n * 128), int(x_c - n * 128), int(x_c + n * 128)]
    return [x_i,x_f,y_i,y_f]

def checkBorder(a, square):
    left,top=False,False
    [x_i, x_f, y_i, y_f] = square
    if(x_i<0):
        left=True
        x_f = x_f-x_i
        x_i = 0
    if (x_f>len(a)):
        assert not left, "no sufiente anchura"
        x_i = x_i + len(a)-1 -x_f
        x_f = len(a) - 1
    if(y_i<0):
        top=True
        y_f = y_f-y_i
        y_i = 0
    if (y_f>len(a[0])):
        assert not top, "no sufiente altura"
        y_i = y_i + len(a[0])-1 -y_f
        y_f = len(a[0]) - 1
    return [x_i, x_f, y_i, y_f]

# def checkPoint(row,square):
#     [x_i, x_f, y_i, y_f] = square
#     [(y_l_e, x_l_e), (y_r_e, x_r_e), _, (y_m_l, x_m_l), (y_m_r, x_m_r)] = \
#         eval(row['keypoints']).values()
#     w,h =x_f-x_i, y_f-y_i
#     #check eyes
#     #altura: 24<x<256-24 ::: 24=256*3/32
#     assert x_i+w*3/32<x_l_e<x_f-w*3/32, 'altura de ojo izquierdo'
#     assert x_i+w*3/32<x_r_e<x_f-w*3/32, 'altura de ojo derech'
#     #anchura:  16<x<256-16 ::: 16=256/16
#     assert y_i + h / 16 < y_r_e < y_f - w * 3 / 32, 'altura de ojo derech'

def makePhotos():
    with open(source + 'Miguel.csv', mode='r') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=csv_columns)
        for row in reader:
            try:
            # print(row)
                img = makePhoto(source, row)
                img.save(source +'edit_img/'+ row['filename'])
            except:
                print('algo')

#getCsv()
makePhotos()
#getCsv('datasets/Cris/')




