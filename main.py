from Modules.showTarifas import showTarifas
import json
import pandas as pd 
from Modules import verificarArchivo, verificarConfig, processFile,dmPeriodos
import csv
import os
import emoji
from pandas import ExcelWriter

mainFile =[]
cfgFiles= ["./resources/tarifa_1.json", "./resources/tarifa_2.json", "./resources/tarifa_3.json", "./resources/tarifa_4.json"]
festivos = './resources/festivo.json'
Tarifa =[]

print('\n')
print("Verificando archivos de configuracion...")
print('\n')

for path in cfgFiles:

    with open (path) as File:
        Tarifa.append(json.load(File))

if verificarConfig.verificar(Tarifa):
    print("Archivo de configuracion invalido")
    input("presiona enter para salir")
    exit()

print("Verificacion terminada....")
print('\n')
print('La informacion sera procesada de acuerdo con los siguientes periodos tarifarios ')
input("presione enter para continuar...")

showTarifas(Tarifa)
with open(festivos) as Festivos:
    fest = json.load(Festivos)

pathFile = input("Introdusca la ruta del archivo a procesar:  ")

try:
    infile = open(pathFile, 'r', errors ='False')
    
except:
    print("error al abrir el archivo ")
    print("Verifique que la ruta y nombre del archivo sea correcta")
    exit()
    

for linea in infile:
    mainFile.append(linea)

pathSalida=pathFile[:-4]+'_proc.xlsx'
infile.close()
print('\n','Procesando... ','\n')
archivoVerificado=verificarArchivo.verificarFile(mainFile)

if type(archivoVerificado) != pd.core.frame.DataFrame:
    exit()

print(emoji.emojize('Archivo verificado :thumbs_up:'))
print(' ')



File=processFile.processF(archivoVerificado,Tarifa,fest)

print('Guardando archivo de excel...')
print('Guardando Hoja GPK...')
#File.to_csv('numeros.csv', header=True, index=False)

writer = ExcelWriter(pathSalida)
File.to_excel(writer, 'GPK', index=False)
writer.save()
print(emoji.emojize('Hoja GPK guardada :thumbs_up:'))

Base = File[File['Periodo'].str.contains('base')].copy()
Intermedia = File[File['Periodo'].str.contains('intermedia')].copy()
Punta = File[File['Periodo'].str.contains('punta')].copy()

dmPeriodos.calDM(Base)

print('Guardando Hoja Base')

Base.to_excel(writer, 'BASE', index=False)
writer.save()

print(emoji.emojize('Hoja BASE guardada :thumbs_up:'))

print('Guardando intermedia')
Intermedia.to_excel(writer, 'INTERMEDIA', index=False)
writer.save()
print(emoji.emojize('Hoja INTERMEDIA guardada :thumbs_up:'))

print('Guardando hoja punta')
Punta.to_excel(writer, 'PUNTA', index=False)
writer.save()
print(emoji.emojize('Hoja PUNTA guardada :thumbs_up:'))

totalKw =File[' "WH3_DEL"'].sum()
totalBase = Base[' "WH3_DEL"'].sum()
totalIntermedia=Intermedia[' "WH3_DEL"'].sum()
totalPunta= Punta[' "WH3_DEL"'].sum()

totalKwComp=totalBase+totalIntermedia+totalPunta

dmBase = Base[' PREV_DM'].max()
dmIntermedia=Intermedia[' PREV_DM'].max()
dmPunta=Punta[' PREV_DM'].max()

if totalKw != totalKwComp:
    print("El procesamiento ha sido incorrecto")
    exit()

print('Total energia entregada a GPK: ',totalKw,' KWH')
print('Total energia Base           : ',totalBase,' KWH')
print('Total energia Intermedia     : ',totalIntermedia,' KWH')
print('Total energia Punta          : ',totalPunta,' KWH')
print('\n')
dataDmBase = Base.loc[Base[' PREV_DM'].idxmax()]
dataDmIntermedia = Intermedia.loc[Intermedia[' PREV_DM'].idxmax()]
dataDmPunta= Punta.loc[Punta[' PREV_DM'].idxmax()]
print('=============================================================')

print('Demanda Maxima base         : ', dmBase)
print(dataDmBase, '\n')
print('=============================================================')
print('Demanda Maxima Intermedia   : ', dmIntermedia)
print(dataDmIntermedia, '\n')
print('=============================================================')
print('Demanda Maxima Punta        : ', dmPunta)
print(dataDmPunta, '\n')

print('Guardando DM...')
dataDmBase.to_excel(writer, 'DM_BASE', index=True, header =True)
writer.save()
print(emoji.emojize('DM Base Guardada :thumbs_up:'))

dataDmIntermedia.to_excel(writer, 'DM_INTERMEDIA', index=True, header=True)
writer.save()
print(emoji.emojize('DM Intermedia Guardada :thumbs_up:'))

dataDmPunta.to_excel(writer, 'DM_Punta', index=True, header=True)
writer.save()
print(emoji.emojize('DM Punta Guardada :thumbs_up:'))


writer.close()