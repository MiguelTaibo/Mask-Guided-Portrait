import python_scripts.correct_labels.timeAnalisie as dinamic
import python_scripts.correct_labels.data as data
import pdb

dt = data.Data()
keyTolabel = dt.keyToLabel

##########PRE FUNCTIONS
def reColourEyes(row, a):
    vecs_nariz = dinamic.strToTupleList(row['Nariz'])
    max_nariz = 0
    th = 10
    nariz = None
    for v in vecs_nariz:
        if v[2] > max_nariz:
            max_nariz = v[2]
            nariz = v

    d_ojo = dinamic.strToTupleList(row['OjoDerecho'])
    for v in d_ojo:
        if v[0]>nariz[0]+th:
            reColour(v,keyTolabel['OjoDerecho'],keyTolabel['Nariz'], a)
        elif v[1]>nariz[1]:
            reColour(v,keyTolabel['OjoDerecho'],keyTolabel['OjoIzquierdo'], a)

    i_ojo = dinamic.strToTupleList(row['OjoIzquierdo'])
    for v in i_ojo:
        if v[0]>nariz[0]+th:
            reColour(v,keyTolabel['OjoIzquierdo'],keyTolabel['Nariz'], a)
        elif v[1]<nariz[1]:
            reColour(v,keyTolabel['OjoIzquierdo'],keyTolabel['OjoDerecho'], a)

    d_ceja = dinamic.strToTupleList(row['CejaDerecha'])
    for v in d_ceja:
        if v[0]>nariz[0]+th:
            reColour(v,keyTolabel['CejaDerecha'],keyTolabel['Nariz'], a)
        elif v[1]>nariz[1]:
            reColour(v,keyTolabel['CejaDerecha'],keyTolabel['CejaIzquierda'], a)

    i_ceja = dinamic.strToTupleList(row['CejaIzquierda'])
    for v in i_ceja:
        if v[0]>nariz[0]+th:
            reColour(v,keyTolabel['CejaIzquierda'],keyTolabel['Nariz'], a)
        elif v[1]<nariz[1]:
            reColour(v,keyTolabel['CejaIzquierda'],keyTolabel['CejaDerecha'], a)

def reColourMouth(row, a):
    vecs_nariz = dinamic.strToTupleList(row['Nariz'])
    max_nariz = 0
    nariz = None
    for v in vecs_nariz:
        if v[2] > max_nariz:
            max_nariz = v[2]
            nariz = v

    labio_superior = dinamic.strToTupleList(row['LabioSuperior'])
    for v in labio_superior:
        if v[0]<nariz[0]:
            reColour(v,keyTolabel['LabioSuperior'],dt.noColor, a)

    interior_boca = dinamic.strToTupleList(row['InteriorBoca'])
    for v in interior_boca:
        if v[0]<nariz[0]:
            reColour(v,keyTolabel['InteriorBoca'],dt.noColor, a)

    labio_inferior = dinamic.strToTupleList(row['LabioInferior'])
    for v in labio_inferior:
        if v[0]<nariz[0]:
            reColour(v,keyTolabel['LabioInferior'],dt.noColor, a)



    x_min = len(a)
    break_bool = False
    for i in range(0,len(a)):
        for j in range(0,len(a[i])):
            if a[i,j]==dt.keyToLabel['LabioSuperior'] or a[i,j]==dt.keyToLabel['LabioInferior']:
                x_min=i
                y_min=j
                #print('x_min = ' + str(x_min))
                break_bool=True
                break
        if break_bool:
            break
    pixelList = []

    for i in range(x_min,len(a)):
        for j in range(0,len(a[1])):
            if a[i,j]==dt.keyToLabel['Nariz']:
                pixelList.append((i,j))
    update_bool = True
    #print(len(pixelList))
    while update_bool:
        update_bool=False
        for (i,j) in pixelList:
            l_int = countArround(a, (i, j), dt.keyToLabel['InteriorBoca'])
            l_inf = countArround(a,(i,j),dt.keyToLabel['LabioInferior'])
            l_sup = countArround(a,(i,j),dt.keyToLabel['LabioSuperior'])
            l = max(l_inf,l_sup,l_int)
            if l !=0:
                update_bool=True
                pixelList.remove((i,j))
                if l ==l_int:   a[i,j]=dt.keyToLabel['InteriorBoca']
                elif l==l_inf:  a[i,j]=dt.keyToLabel['LabioInferior']
                elif l==l_sup:  a[i,j]=dt.keyToLabel['LabioSuperior']
                else:
                    print('Whuuuuut??????')
    for i in range(x_min+1,0,-1):
        if a[i,y_min]==dt.keyToLabel['Nariz']:
            x_max = i
            break
    for i in range(x_max, len(a)):
        for j in range(0,len(a[i])):
            if a[i,j]==dt.keyToLabel['Nariz']:
                a[i,j]=dt.keyToLabel['Cara']




def reColour(v, labeli, labelf, img):
    v_x, v_y = int(v[0]), int(v[1])
    #print(str(v) + ' : ' + str(labeli)+ ' to ' + str(labelf))
    x,y=v_x, v_y
    # Buscamos en 4 direcciones el pixel más cercano al centroide,
    # aunque lo mas comun sera que el centroide este dentro
    for i in range(128):
        if (v_x + i < len(img) and img[v_x + i, v_y] == labeli):
            x, y = v_x + i, v_y
            break
        elif (v_x - i > -1 and img[v_x - i, v_y] == labeli):
            x, y = v_x - i, v_y
            break
        elif (v_y + i < len(img[v_x]) and img[v_x, v_y + i] == labeli):
            x, y = v_x, v_y + i
            break
        elif (v_y - i > -1 and img[v_x, v_y - i] == labeli):
            x, y = v_x, v_y - i
            break

    pixelList = [(x, y)]
    img[x][y] = labelf
    # print(x,y)
    index = 0
    n = 1
    while index < len(pixelList):
        newPixels = pixelsArround(img, pixelList[index], labeli)
        # print(str(index) + ' , ' + str(newPixels))
        for (i, j) in newPixels:
            img[i, j] = labelf
            n += 1
            pixelList.append((i, j))
        index += 1
    if (n == v[2]):
        return True
    else:
        return n

def pixelsArround(a, pixel, label):
    res=[]
    x,y = pixel[0],pixel[1]
    for i in range(x-1,x+2):
        if (i==len(a)):
            continue
        for j in range(y-1,y+2):
            if (j==len(a[i])):
                continue
            if (i==x and j==y):
                continue
            if (a[i,j]==label):
                res.append((i,j))
    return res

def countArround(a,pixel,label):
    count = 0
    x,y = pixel[0],pixel[1]
    for i in range(x-1,x+2):
        if (i==len(a)):
            continue
        for j in range(y-1,y+2):
            if (j==len(a[i])):
                continue
            if (i==x and j==y):
                continue
            if (a[i,j]==label):
                count+=1
    return count

###########POST FUNCTIONS
def reColourCara(row,img):
    d_ceja = dinamic.strToTupleList(row['CejaDerecha'])
    l_d = 0
    for v in d_ceja:
        if v[2]>l_d:
            l_d = v[2]
    i_ceja = dinamic.strToTupleList(row['CejaIzquierda'])
    l_i = 0
    for v in i_ceja:
        if v[2]>l_i:
            l_i = v[2]

    nariz_vecs = dinamic.strToTupleList(row['Nariz'])
    nariz_len = 0
    nariz = None
    for v in nariz_vecs:
        if v[2] > nariz_len:
            nariz = v
            nariz_len = v[2]

    if l_i>2*l_d:
        #print('izquierda : ' + str(l_i) + '      derecha : ' +str(l_d))
        step, st , end, boolean = -1,int(nariz[1]), 0, True
    elif l_d>2*l_i:
        #print('izquierda : ' + str(l_i) + '      derecha : ' + str(l_d))
        step, st, end, boolean = 1, int(nariz[1]), len(img[0]),True
    else:
        step, st, end, boolean  = 1,0,0,False




    if boolean:
        #pelo de la parte de la nariz
        for i in range(int(nariz[0]-len(img)/8), int(nariz[0])):
            for j in range(st,end,step):
                if img[i,j]==dt.keyToLabel['Pelo']:
                    img[i,j]=dt.keyToLabel['Fondo']

        #Nariz
        min_nariz=7
        th_nariz = 15
        break_bool = False
        for i in range(len(img)-1,-1,-1):
            for j in range(end,st,step*-1):
                if img[i,j]==dt.keyToLabel['Nariz']:
                    (x,y)=(i,j)
                    break_bool = True
                    break
            if break_bool:
                break
        b_buffer = None
        b_bool = False
        temp_step = step
        for b in range(y+step*x,128*(1-step),-step):
            count = lookInDiagonal(img,b,step)
            if count < min_nariz:
                b_buffer = b
            elif count > th_nariz:
                b_bool=True
                break
            elif count== 0:
                break
        #pdb.set_trace()
        if b_bool and b_buffer!=None:
            for b in range(b_buffer,128*(1+3*step),step):
                removeDiagonal(img,b,step)

        #parte superior a la nariz
        relleno = 0
        for j in range(st,end,step):
            for i in range(0,int(nariz[0])+10):
                if (img[i,j]==dt.keyToLabel['CejaDerecha'] or img[i,j]==dt.keyToLabel['CejaIzquierda'] or \
                        img[i, j] == dt.keyToLabel['OjoDerecho'] or img[i, j] == dt.keyToLabel['OjoIzquierdo']) \
                        and  img[i+1, j]==dt.keyToLabel['Fondo']:
                    labels = [dt.keyToLabel['Cara'],dt.keyToLabel['OjoDerecho'],dt.keyToLabel['OjoIzquierdo']]
                    x,temp_bool = lookInLine(img, (i,j),labels)
                    if temp_bool:
                        for i2 in range(i,x):
                            relleno+=1
                            img[i2,j]=dt.keyToLabel['Cara']
                elif img[i,j]==dt.keyToLabel['Cara'] and img[i+1, j]==dt.keyToLabel['Fondo']:
                    labels = [dt.keyToLabel['CejaIzquierda'],dt.keyToLabel['CejaDerecha'], dt.keyToLabel['OjoDerecho'], dt.keyToLabel['OjoIzquierdo']]
                    x, temp_bool = lookInLine(img, (i, j), labels)
                    if temp_bool:
                        for i2 in range(i, x):
                             if  img[i2, j]==dt.keyToLabel['Fondo']:
                                 relleno += 1
                                 img[i2, j] = dt.keyToLabel['Cara']
        el = 0
        for j in range(st,end,step):
            for i in range(0,int(nariz[0]+50)):
                if img[i,j]==dt.keyToLabel['Cara']:
                    if i<nariz[0]:
                        altura=0
                        l = 8
                    else:
                        altura = 1
                        l = 5

                    if not iterTriangleLabel(img,(i,j),step, altura, l1=l):
                        img[i,j]=dt.keyToLabel['Fondo']
                        el +=1
        #print('Eliminamos :' + str(el))

        #Parte inferior a la nariz
        for i in range(len(img)-1,0,-1):
            if img[i,int(nariz[1])]==dt.keyToLabel['Nariz']:
                x_min_nariz=i
                break


        min_heigh = 30
        for j in range(st,end,step):
            count = 0
            for i in range(int(nariz[0]),len(img),1):
                if img[i,j]!=dt.keyToLabel['Fondo'] and  img[i,j]!=dt.keyToLabel['Pelo']:
                    count+=1
            if count<min_heigh:
                for i in range(x_min_nariz,len(img)):
                    if img[i,j]==dt.keyToLabel['Cara']:
                        img[i,j]=dt.keyToLabel['Fondo']

        #parte superior a la nariz
        el = 0
        for j in range(st,end,step):
            for i in range(0,int(nariz[0]+64)):
                if img[i,j]==dt.keyToLabel['Cara']:
                    if i<nariz[0]:
                        altura=0
                        l = 8
                    else:
                        altura = 1
                        l = 1

                    if not iterTriangleLabel(img,(i,j),step, altura, l1=l):
                        img[i,j]=dt.keyToLabel['Fondo']
                        el +=1


        # min_heigh = 30
        # eliminados = []
        # for j in range(st,end,step):
        #     #min_heigh += 1
        #     found, count, inicio = continueInColumn(img, j, dt.keyToLabel['Cara'], index=int(nariz[0])-10)
        #     while found:
        #         pdb.set_trace()
        #         if count < min_heigh:
        #             #fondo to fondo or nariz -> fondo
        #             if img[inicio, j] == dt.keyToLabel['Fondo'] and \
        #                     (img[inicio - count - 1, j] == dt.keyToLabel['Fondo'] or img[inicio - count - 1, j] ==
        #                      dt.keyToLabel['Nariz']):
        #                 eliminados.append((inicio,count,j))
        #                 min_heigh += count
        #                 #print(min_heigh)
        #                 for i in range(inicio - count, inicio):
        #                     img[i, j] = dt.keyToLabel['Fondo']
        #             # #nariz to nariz o fondo -> nariz
        #             # elif img[inicio, j] == dt.keyToLabel['Nariz'] and \
        #             #         (img[inicio - count - 1, j] == dt.keyToLabel['Fondo'] or img[inicio - count - 1, j] ==
        #             #          dt.keyToLabel['Pelo']):
        #             #     eliminados.append((inicio, count, j))
        #             #     for i in range(inicio-count, inicio):
        #             #         img[i, j] = dt.keyToLabel['Nariz']
        #             # pelo to fondo or nariz -> fondo
        #             elif img[inicio, j] == dt.keyToLabel['Pelo'] and \
        #                     (img[inicio - count - 1, j] == dt.keyToLabel['Fondo'] or img[inicio - count - 1, j] ==
        #                      dt.keyToLabel['Nariz']):
        #                 eliminados.append((inicio, count, j))
        #                 for i in range(inicio - count, inicio):
        #                     img[i, j] = dt.keyToLabel['Fondo']
        #                 min_heigh += count
        #
        #         if inicio == len(img) - 1:
        #             break
        #         else:
        #             found, count, inicio = continueInColumn(img, j, dt.keyToLabel['Cara'], index=inicio)

        # nariz_vecs = dinamic.strToTupleList(row['Nariz'])
        # nariz_len = 0
        # nariz = None
        # for v in nariz_vecs:
        #     if v[2]> nariz_len:
        #         nariz = v
        #         nariz_len = v[2]
        # eliminado_arriba = None
        # eliminado_abajo = None
        # for el in eliminados:
        #     if eliminado_arriba == None and el[0]<nariz[0]:
        #         eliminado_arriba = el
        #     elif eliminado_abajo ==  None and el[0]-el[1]>nariz[0]:
        #         eliminado_abajo = el
        #
        # if eliminado_abajo!=None:
        #     el = eliminado_abajo
        #     x_i,x_f,y_i,y_f=el[0]-el[1],len(img),el[2],end
        #     for i in range(x_i,x_f):
        #         for j in range(y_i,y_f,step):
        #             if img[i,j]==dt.keyToLabel['Cara']:
        #                 img[i,j]=dt.keyToLabel['Fondo']
        # if eliminado_arriba!=None:
        #     el = eliminado_arriba
        #     x_i,x_f,y_i,y_f=0,el[0],el[2],end
        #     for i in range(x_i,x_f):
        #         for j in range(y_i,y_f,step):
        #             if img[i,j]==dt.keyToLabel['Cara']:
        #                 img[i,j]=dt.keyToLabel['Fondo']


def iterTriangleLabel(img, pixel, step, altura, l1=8):
    (i,j)=pixel
    res = True
    for t in range(1,l1+1):
        j2 = j-t*step
        if altura==0 and  (img[i - 2*t, j2] == keyTolabel['Fondo'] or img[i -2*t+1, j2] == keyTolabel['Fondo'] or \
                    img[i + 2*t-1, j2] == keyTolabel['Fondo'] or img[i + 2*t, j2] == keyTolabel['Fondo']):
                #print(t)
                res = False
        elif altura==1  and ((img[i - 2*t, j2] == keyTolabel['Fondo'] or img[i -2*t+1, j2] == keyTolabel['Fondo'] or \
                    img[i + 2*t-1, j2] == keyTolabel['Fondo'] or img[i + 2*t, j2] == keyTolabel['Fondo']) or \
                (img[i - 2 * t, j2] == keyTolabel['Pelo'] or img[i - 2 * t + 1, j2] == keyTolabel['Pelo'] or \
                 img[i + 2 * t - 1, j2] == keyTolabel['Pelo'] or img[i + 2 * t, j2] == keyTolabel['Pelo'])):
            res = False
    return res

def lookInLine(img, pixel,labels):
    (x,y)=pixel
    for i in range(x+1,len(img)):
        if img[i,y]==dt.keyToLabel['Fondo']:
            continue
        elif labels.count(img[i,y])!=0:
            return i, True
        else:
            return i, False
    return i,False

def lookInDiagonal(img, b, step, label=dt.keyToLabel['Nariz']):
    count=0
    for x in range(len(img)):
        y = -step*x+b
        if y>-1 and y<len(img[x]):
            if img[x,y]==label:
                count+=1
    return count

def removeDiagonal(img,b,step, labeli=dt.keyToLabel['Nariz'], labelf=dt.keyToLabel['Cara']):
    res = False
    for x in range(len(img)):
        y = -step * x + b
        if y > -1 and y < len(img[x]):
            if img[x, y] == labeli:
                img[x,y] = labelf
                res = True
    return res

def continueInColumn(img,y,label, index=0):
    count = 0
    found = False
    for i in range(index,len(img)):
        if img[i,y]==label:
          found=True
          break
    for i2 in range(i,len(img)):
        if img[i2,y]==label:
            count+=1
        else:
            break
    return found, count, i2

