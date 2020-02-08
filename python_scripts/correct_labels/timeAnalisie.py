import python_scripts.correct_labels.remake as rmk

# Leyenda de restricctiones:
# 0 : numero de intervalos compactos posibles
# 1 :
dic_res= {
    'filename' : [100],
    'Fondo' : [1],
    'Cara' : [1],
    'CejaDerecha' : [1],
    'CejaIzquierda' : [1],
    'OjoDerecho' : [1],
    'OjoIzquierdo' : [1],
    'Nariz' : [1],
    'LabioSuperior' : [1],
    'InteriorBoca' : [1],
    'LabioInferior' : [1],
    'Pelo' : [1]
}

def searchProblemsInFrame(row):
    problems = []
    for k,v in row.items():
        if (v.count('(')>dic_res[k][0]):
            problems.append(k)
            #print(str(k) + ':' + str(v.count('(')))
            #print(v)
    return problems

def searchProblems(reader):
    problems = []
    for row in reader:
        problems.append(searchProblemsInFrame(row))
    return problems

def correctProblems(row, buffer, etapa):
    pr = searchProblemsInFrame(row)
    for k in pr:
        #print(row)
        v = decideProblem(row,buffer,k, etapa)
        row[k] = v
        #if len(v)>dic_res[k][0] and (k=='Nariz' or k=='Cara'):
        #    print('No prediccion en '+ row['filename'] + ' , '+ k)

    # registros de filas anteriores
    buffer[2] = buffer[1]
    buffer[1] = buffer[0]
    buffer[0] = row
    return row, buffer

def decideProblem(row, buffer, k, etapa):
    #if etapa=='preanalisis':
    if k=='Nariz':
        v = positionNariz(row[k],buffer,k)
    elif etapa=='analisis':
        if k=='CejaDerecha':
            v = positionEye(row[k],buffer,k)
        elif k=='CejaIzquierda':
            v = positionEye(row[k],buffer,k)
        elif k=='OjoDerecho':
            v = positionEye(row[k],buffer,k)
        elif k=='OjoIzquierdo':
            v = positionEye(row[k],buffer,k)
        elif k=='LabioSuperior' or k =='LabioInferior':
            v = positionLabio(row[k],buffer,k)
        elif k == 'Cara':
            v = masGrande(row, k)
        elif k == 'Pelo':
            v = minLength(row, k)
        elif k == 'Fondo':
            v = minLengthLado(row, k)
        else:
            v = row[k]
    else:
        v = row[k]
    return v


####################################################################################################
####################        CRITERIOS DE DECISION DE CONJUNTO COMPACTO          ####################
####################                                                            ####################
####################################################################################################
####################################################################################################


# def positionPrediction(vectores, buffer, k):
#     #v1,v2,v3=buffer[0][k],buffer[1][k],buffer[2][k]
#     v1_temp = buffer[0][k]
#     dist = []
#     dmin = 1000000000
#     value = None
#     #v1 = strToTupleList(v1_temp)[0]
#     try:
#         v1 = strToTupleList(v1_temp)[0]
#     except:
#         try:
#             v1 = strToTupleList(str(v1_temp))[0]
#         except:
#             #Aqui se llega si en el frame anterior no habia nada
#             return vectores
#     #v1 = strToTupleList(v1)[0]
#     vectores = strToTupleList(vectores)
#     #Calculamos la posición prevista como igual a la anterior
#     v_x = v1[0]
#     v_y = v1[1]
#     #calculamos la posición prevista usando una aceleracion constante
#     #v_x = 3*v1[0]-3*v2[0]+v3[0]
#     #v_y = 3*v1[1]-3*v2[1]+v3[1]
#     #Calculamos las distintas distancias
#     for v in vectores:
#         d = (v_x-v[0])*(v_x-v[0])+(v_y-v[1])*(v_y-v[1])
#         if (d < dmin):
#             dmin = d
#             value = v
#         dist.append(d)
#     #print('value : ' + str(value))
#     return [value]

def positionNariz(vectores, buffer, k, t_trian = 10, d_trian=7, heigh=10):
    v1_temp = buffer[0][k]
    vectores = strToTupleList(vectores)
    values = []
    try:
        v1 = strToTupleList(v1_temp)[0]
    except:
        try:
            v1 = strToTupleList(str(v1_temp))[0]
        except:
            return vectores
    for v in vectores:
         try:
            if d_trian*abs(v1[1]-v[1])+abs(v1[0]-v[0])<(d_trian+1)*t_trian and abs(v1[0]-v[0])<heigh:
                values.append(v)
         except:
            print(vectores)
            exit()
    return values

def cejaPrediction(row, buffer, k, lmin=10, dmax=10):
    values = []
    vectores = strToTupleList(row[k])
    v1_temp = buffer[0][k]
    try:
        v1 = strToTupleList(v1_temp)[0]
    except:
        v1 = strToTupleList(str(v1_temp))[0]
    v_x = v1[0]
    v_y = v1[1]
    for v in vectores:
        if v[3]<lmin:
            vectores.remove(v)
    for v in vectores:
        d = abs(v_x - v[0])+ abs(v_y - v[1])
        if (d < dmax):
            values.append(v)
    return values

def masGrande(row, k):
    #img = rmk.openFilename(row['filename'])
    #label = rmk.keyToLabel(k)
    max_index = 0
    value = None
    try:
        conj_list = strToTupleList(row[k])
    except:
        conj_list = strToTupleList(str(row[k]))
    for v in conj_list:
        if (v[2]>max_index):
            max_index=v[2]
            value = v
    return [value]

def minLengthLado(row, k, min_len = 1536):
    res = []
    try:
        conj_list = strToTupleList(row[k])
    except:
        conj_list = strToTupleList(str(row[k]))
    for v in conj_list:
        if (v[2] > min_len - 3*(abs(v[0]-128)+abs(v[1]-128))):
            res.append(v)
    return res

def minLength(row, k, min_len = 300):
    res = []
    try:
        conj_list = strToTupleList(row[k])
    except:
        conj_list = strToTupleList(str(row[k]))
    for v in conj_list:
        if (v[2]>min_len):
            res.append(v)
    return res

def positionLabio(vectores,buffer,k, width=60, heigh=20):
    return positionEye(vectores, buffer, k, width=width, heigh=heigh)

def positionEye(vectores,buffer,k, width = 40, heigh = 20):
    v1_temp = buffer[0][k]
    vectores = strToTupleList(vectores)
    values = []
    try:
        v1 = strToTupleList(v1_temp)[0]
    except:
        try:
            v1 = strToTupleList(str(v1_temp))[0]
        except:
            return vectores
    for v in vectores:
         try:
            if abs(v1[1]-v[1])<heigh and abs(v1[0]-v[0])<width:
                values.append(v)
         except:
            print(vectores)
            exit()
    return values

#######################################################
##########  Funcion auxiliares de decision   ##########
#######################################################
def countPixelConj(v,img,label):
    v_x, v_y = int(v[0]), int(v[1])
    for i in range(128):
        if (v_x + i < len(img) and img[v_x + i][v_y] == label):
            x, y = v_x + i, v_y
            break
        elif (v_x + i > -1 and img[v_x - i][v_y] == label):
            x, y = v_x - i, v_y
            break
        elif (v_y + i < len(img[v_x]) and img[v_x][v_y + i] == label):
            x, y = v_x, v_y + i
            break
        elif (v_y - i < len(img[v_x]) and img[v_x][v_y - i] == label):
            x, y = v_x, v_y - i
            break

    pixelList = [(x, y)]
    index = 0
    while index < len(pixelList):
        newPixels = pixelsArround(img, pixelList[index], label)
        for e in newPixels:
            if (pixelList.count(e) == 0):
                pixelList.append(e)
        index += 1
    return v, index

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

#Convierte un string con el formato correcto a una lista de tuples
def strToTupleList(str):
    s = str[1:len(str)-1]
    tuple_res = []
    if s == '':
        return tuple_res
    s = s.split(')')
    for e in s:
        n = e.find('(')
        if (n!=-1):
            s_temp = e[n+1:len(e)]
            s_temp = s_temp.split(',')
            tuple_temp = (float(s_temp[0]),float(s_temp[1]),int(s_temp[2]))
            tuple_res.append(tuple_temp)
    return tuple_res

def strToTuple(str):
    s = str[1:len(str)-1]
    s_temp = s.split(',')
    return (float(s_temp[0]),float(s_temp[1]),int(s_temp[2]))


# #Esto devuelve el primer valor si hay varios
# def strsToTuples(str1,str2,str3):
#     return strToTupleList(str1)[0],strToTupleList(str2)[0],strToTupleList(str3)[0]
