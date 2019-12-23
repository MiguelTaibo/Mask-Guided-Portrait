import csv
import sys, os, shutil
import numpy as np
from PIL import Image

def make_csv(th):

    with open('/mnt/pgth04b/Data_Miguel/DATASETS/AFFECTNET/Manually_Annotated_file_lists_ORIGINAL/training.csv',
              mode='r') as csv_file_ori:
        with open('/mnt/pgth04b/Data_Miguel/DATASETS/AFFECTNET/Manually_Annotated_file_lists_ORIGINAL/training1.csv',
                  mode='w') as csv_file_dest:
            nHappy = 0
            nSad = 0
            csv_reader = csv.DictReader(csv_file_ori, delimiter=',')
            print(csv_reader.fieldnames)
            csv_writer = csv.DictWriter(csv_file_dest, csv_reader.fieldnames)
            csv_writer.writerow(csv_reader.fieldnames)
            for row in csv_reader:
                # print(row_read['face_x'])
                # break
                if (int(row['expression']) == 1):  # happy
                    if nHappy < th:
                        nHappy += 1
                        csv_writer.writerow(row)
                elif (int(row['expression']) == 2):  # sad
                    if nSad < th:
                        nSad += 1
                        csv_writer.writerow(row)
                else:
                    continue
            print(nHappy)
            print(nSad)


def getImages():
    with open('/mnt/pgth04b/Data_Miguel/DATASETS/AFFECTNET/Manually_Annotated_file_lists_ORIGINAL/training1.csv',
              mode='r') as csv_file:
        with open('/mnt/pgth04b/Data_Miguel/DATASETS/AFFECTNET/Manually_Annotated_file_lists_ORIGINAL/training2.csv',
                  mode='w') as csv_file_dest:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            csv_writer = csv.DictWriter(csv_file_dest, csv_reader.fieldnames)
            #csv_writer.writerow(csv_reader.fieldnames)
            imgAddr, desAddr = '',''

            for row in csv_reader:

                imgAddr = '/mnt/pgth04b/Data_Miguel/DATASETS/AFFECTNET/Manually_Annotated_compressed_ORIGINAL/Manually_Annotated_Images/' + str(row['subDirectory_filePath'])

                ni, nf = row['subDirectory_filePath'].find('/') + 1,row['subDirectory_filePath'].find('.jpg')+4
                row['subDirectory_filePath'] = row['subDirectory_filePath'][ni:nf]

                desAddr = '/mnt/pgth04b/Data_Miguel/DATASETS/AFFECTNET/Manually_Annotated_compressed_ORIGINAL/images/' + str(row['subDirectory_filePath'])
                csv_writer.writerow(row)
                shutil.copy(imgAddr, desAddr)

#def parseLabel(row):


# make_csv(csv_file_ori,csv_file_dest, 25000)
# getImages()

with open('/home/migueltaibo/Mask_Guided_Portrait_Editing/datasets/training2.csv',
          mode='r') as csv_file_ori:
    csv_reader = csv.DictReader(csv_file_ori, delimiter=',')
    for row in csv_reader:
        if(str(row['subDirectory_filePath'])=='5c991a28b5550cf5e1e830d5eed1dc7f80581462d6278c873c1c9db6.jpg'):
            linea = row
            break

img = Image.open('./datasets/images/' + str(row['subDirectory_filePath']))
a = np.array(img)
landmarks = linea['facial_landmarks'].split(';')
control = True;
for i in landmarks:
    if control:

        x = round(float(i))
    else:
        y = round(float(i))
        #print(str(x)+","+str(y))
        a[y][x]=[255,255,255]
    control = not control


#print(a[223][25])
img = Image.fromarray(a)
img.show()
#a = np.array(img)
#print(a.shape)
#img.resize((256,256)).show()

##FOTO PRUEBA
##5c991a28b5550cf5e1e830d5eed1dc7f80581462d6278c873c1c9db6.jpg,35,35,236,236,46.5;134.89;47.28;158.87;51.45;182.31;58.37;206.89;69.99;230.59;86.89;249.66;109.6;266.35;132.0;279.94;160.37;280.24;186.65;275.91;206.48;259.74;223.65;241.27;237.19;219.04;243.34;195.03;246.9;170.62;248.02;146.81;247.05;125.14;65.45;119.13;80.0;108.4;98.92;106.32;117.51;109.64;136.22;114.91;172.84;111.31;190.84;104.21;206.81;100.96;223.19;99.36;237.21;105.95;155.61;129.33;156.73;145.98;158.37;163.09;159.75;180.06;139.23;192.82;149.05;195.01;158.78;198.42;167.55;194.79;176.61;190.5;87.75;132.75;98.06;124.59;112.84;123.67;123.52;133.18;112.06;137.42;97.94;138.11;182.79;129.25;193.04;118.56;206.64;117.29;216.22;124.19;209.23;130.83;196.07;131.88;117.66;224.95;131.58;221.12;147.77;216.23;158.1;218.05;169.08;214.44;184.58;216.53;198.83;218.29;186.27;230.08;171.98;235.16;160.84;237.33;150.13;237.39;134.68;233.94;125.52;226.73;148.39;226.41;158.73;225.88;169.96;224.44;192.33;221.26;170.7;221.52;159.64;223.35;149.7;223.25,1,0.547918,0.249054
