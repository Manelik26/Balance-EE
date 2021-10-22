import pandas as pd 
import datetime as dt
from datetime import timedelta

def verificarFile(File):
    archivoSalida =[]
    header=''
    finalHeader=[' Date', ' Time', ' "WH3_DEL"',  ' "QH3_DEL"' ]
    quinceMinutal=[]
    for linea in File: 
        lineaPiv = linea.split(',',20)
        if lineaPiv[0]== 'Record'or header== True:
            header = True
            lineaPiv.pop(7)
            lineaPiv.pop(6)
            lineaPiv.pop(5)
            lineaPiv.pop()
            lineaPiv.pop()
            lineaPiv.pop()
            lineaPiv.pop()
            lineaPiv.pop()
            lineaPiv.pop()
            lineaPiv.pop()
            lineaPiv.pop(0)
            lineaPiv.pop(2)

            archivoSalida.append((lineaPiv))
            
    piv = archivoSalida[0]
    
    serie= pd.DataFrame(archivoSalida,columns =finalHeader)
    
    serie = serie.drop(0)
   
    serie.insert(1,' DateTime', serie[' Date']+ serie[' Time'] )
    
    serie[' "WH3_DEL"']=serie[' "WH3_DEL"'].astype(float)
    serie[' "QH3_DEL"']=serie[' "QH3_DEL"'].astype(float)
    serie.insert(5,' KW_DEL',serie[' "WH3_DEL"']*60)

    serie[ ' DateTime']= serie[' DateTime'].apply(lambda x: dt.datetime.strptime(x, ' %m/%d/%Y %H:%M:%S'))

    serie.drop([' Date', ' Time'], axis= 'columns', inplace = True)

    if  verificarSerie(serie[' DateTime'])>300:
        return 600
    
    return serie

def verificarSerie ( serie):
    verificador = 0
    
    if serie[1].minute !=0 or serie[1].hour  != 7 :
        print("Error en la fecha inicial ", serie[1])
        return 601
    
    if serie[len(serie)].minute != 59 or serie[len(serie)].hour != 6 :
        print("Error en la fecha final ", serie[len(serie)])
        return 602
    
    for elemento in serie:
        if verificador != 0:
            if verificador != elemento - timedelta(minutes=1) :

                if verificador == elemento -timedelta(minutes=1,hours =1) or verificador == elemento +timedelta(minutes = 59) :
                    print('Encontrada secuencia de cambio de horario')
                    print('De: ', verificador, ' a: ',elemento, '\n')
                else:
                    print("Error en secuencia de fechas y horas a las: ", verificador)
                    return 600
                

                
        verificador = elemento 
    
    return 200
