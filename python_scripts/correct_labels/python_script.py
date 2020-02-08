import python_scripts.correct_labels.getCsv as sc
import os
dt = sc.data.Data()

sc.diccionarysToCsv(dt.pre_analisis)
sc.filterLabels('preanalisis')
sc.preColour()
os.system('cp otros/* otros_preanalisis/')
sc.diccionarysToCsv(dt.analisis)
sc.filterLabels('analisis')
sc.reColourAll()
os.system('cp otros/* otros_analisis/')
sc.diccionarysToCsv('tAnalisis3')
sc.postColour()
os.system('cp otros/* otros_postanalisis/')
sc.diccionarysToCsv('tAnalisis4')