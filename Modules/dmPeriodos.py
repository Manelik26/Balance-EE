import pandas as pd
pd.set_option('mode.chained_assignment', None) #Asignacion encadenada 'None'
def calDM (FileB):

    miTarifa =[]
    FIFO =[]
    pivFile =FileB[' KW_DEL']
    archivoRetorno =[]

    for element in pivFile:
        FIFO.append(element)

        if len(FIFO)<15:
            archivoRetorno.append(0.0)
        else:
                
            archivoRetorno.append(sum(FIFO)/15)
            FIFO.pop(0)
        
    FileB['DM_Periodo']=archivoRetorno