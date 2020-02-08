class Data:
    #def __init__(self):
    source = 'datasets/exp2/otros/'
    noColor = 11
    name = 'tModificados'
    pre_analisis = 'tAnalisis'
    analisis = 'tAnalisis2'

    csv_columns = ['filename', 'Fondo', 'Cara', 'CejaDerecha', 'CejaIzquierda',
                   'OjoDerecho', 'OjoIzquierdo', 'Nariz', 'LabioSuperior',
                   'InteriorBoca', 'LabioInferior', 'Pelo']
    corrected_columns = ['Nariz','OjoDerecho','OjoIzquierdo',
                         'CejaDerecha','CejaIzquierda',
                         'Cara', 'Pelo', 'Fondo']
    keyToLabel = {
        'Fondo' : 0,
        'Cara' : 1,
        'CejaDerecha' : 2,
        'CejaIzquierda' : 3,
        'OjoDerecho' : 4,
        'OjoIzquierdo' : 5,
        'Nariz' : 6,
        'LabioSuperior' : 7,
        'InteriorBoca' : 8,
        'LabioInferior' : 9,
        'Pelo': 10
    }
