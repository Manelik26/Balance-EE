import pandas as pd
import datetime as dt

def processF (File, Tarifa, fest):
    
    miTarifa =[]
    FIFO =[]
    pivFile =File[' KW_DEL']
    archivoRetorno =[]

    for element in pivFile:
        FIFO.append(element)

        if len(FIFO)<15:
            archivoRetorno.append(0.0)
        else:
            
            archivoRetorno.append(sum(FIFO)/15)
            FIFO.pop(0)
    
    File[' PREV_DM']=archivoRetorno

    #print('DM: ',max(File[' PREV_DM']), ' KW')
    #print(File.loc[File[' PREV_DM'].idxmax()], '\n')

    dicTarifas =[]

    dicTarifas=(seleccionTarifa(File,Tarifa, fest))
    print('Procesamiento terminado                      ', dt.datetime.now().time())
    return File

def seleccionTarifa (File, Tarifa,fest):

    periodo_1_inicio = dt.datetime.strptime(Tarifa[0]['vigencia']['inicio'],'%d/%m/%Y' )
    periodo_1_final = dt.datetime.strptime(Tarifa[0]['vigencia']['final'], '%d/%m/%Y') + dt.timedelta(days =1)
        
    periodo_2_inicio = dt.datetime.strptime(Tarifa[1]['vigencia']['inicio'],'%d/%m/%Y' )
    periodo_2_final = dt.datetime.strptime(Tarifa[1]['vigencia']['final'], '%d/%m/%Y') + dt.timedelta(days =1)

    periodo_3_inicio = dt.datetime.strptime(Tarifa[2]['vigencia']['inicio'],'%d/%m/%Y' )
    periodo_3_final = dt.datetime.strptime(Tarifa[2]['vigencia']['final'], '%d/%m/%Y') + dt.timedelta(days =1)

    periodo_4_inicio = dt.datetime.strptime(Tarifa[3]['vigencia']['inicio'],'%d/%m/%Y' )
    periodo_4_final = dt.datetime.strptime(Tarifa[3]['vigencia']['final'], '%d/%m/%Y') + dt.timedelta(days =1)

    periodoHoras =[]
    periodoHorasPiv =[]
    T1=[]
    T2=[]
    T3=[]
    T4=[]
    columnaPeriodo=[]
    print('Procesando configuracion.....  ')
    for i in range(0,4,1):
        for horas in Tarifa[i]['tarifas'].values():    
            
            for horario in horas.values():
                
                periodoHorasPiv.append(horario)
                
            periodoHoras.append(list(periodoHorasPiv))
            periodoHorasPiv = []
             
    for i in range(0,len(periodoHoras),1):

        if i>=27 and i<36:
            T4.append(periodoHoras[i])
        if i >=18 and i<27:
            T3.append(periodoHoras[i])
        if i >=9 and i<18:
            T2.append(periodoHoras[i])
        if i>=0 and i<9 :
            T1.append(periodoHoras[i])
    
    toTime(T1)
    toTime(T2)
    toTime(T3)
    toTime(T4)
            
    print('Archivo de configuracion procesado')

    print('iniciando procesamiento de archivo csv....', dt.datetime.now().time())
    for element in File[' DateTime']:
        
        #Verificacion de periodo 1 
        
        if element >= periodo_1_inicio and element < periodo_1_final:
            #print('en primer periodo')
            periodo = selTarifaHora(element,T1,fest)
            columnaPeriodo.append(periodo)
            continue
        
        #Verificacion de periodo 2
        if element >= periodo_2_inicio and element < periodo_2_final:
            #print('en segundo periodo')
            periodo = selTarifaHora(element,T2,fest)
            columnaPeriodo.append(periodo)
            continue
        
        #Verificacion periodo 3
        if element >= periodo_3_inicio and element < periodo_3_final:
            print('en tercer periodo')
            periodo = selTarifaHora(element,T3,fest)
            columnaPeriodo.append(periodo)
            continue
        
        #Verificacion periodo 4
        if element >= periodo_4_inicio and element < periodo_4_final:
            print('en cuarto periodo')
            periodo = selTarifaHora(element,T4,fest)
            columnaPeriodo.append(periodo)
            continue
        
        

    File['Periodo']=columnaPeriodo
    

def selTarifaHora( registro, periodoHoraT , fest):
           
    pvPeriodoHoraT = pd.DataFrame(periodoHoraT, columns =['tarifa', 'inicio_1','final_1', 'inicio_2', 'final_2', 'inicio_3', 'final_3'])
    diaSemana = dt.datetime.isoweekday(registro)
    ## Pendiente verificar dia festivo 

    
    for fecha in fest['festivos'].values():
        
        piv= dt.datetime.strptime(fecha, '%d/%m/%Y').date()
        
        if registro.date()==piv:
            diaSemana=7
            break


    
    if diaSemana < 6 :
        
        for columna in range(0,3,1):
            
            if periodoHoraT[columna][1]:
                

                if registro.time() >= periodoHoraT[columna][1] and registro.time() <= periodoHoraT[columna][2]:
                    
                    return periodoHoraT[columna][0]
           
            if periodoHoraT[columna][3]:
                

                if registro.time() >= periodoHoraT[columna][3] and registro.time() <= periodoHoraT[columna][4]:
                    
                    return periodoHoraT[columna][0]
            
            if periodoHoraT[columna][5]:
                

                if registro.time() >= periodoHoraT[columna][5] and registro.time() <= periodoHoraT[columna][6]:
                    
                    return periodoHoraT[columna][0]
            
            
    elif diaSemana == 6 :
    
        for columna in range (3,6,1):
            if periodoHoraT[columna][1]:
                

                if registro.time() >= periodoHoraT[columna][1] and registro.time() <= periodoHoraT[columna][2]:
                    
                    return periodoHoraT[columna][0]
           
            if periodoHoraT[columna][3]:
                

                if registro.time() >= periodoHoraT[columna][3] and registro.time() <= periodoHoraT[columna][4]:
                    
                    return periodoHoraT[columna][0]
            
            if periodoHoraT[columna][5]:
              

                if registro.time() >= periodoHoraT[columna][5] and registro.time() <= periodoHoraT[columna][6]:
                    
                    return periodoHoraT[columna][0]
    
    #if diaSemana == 7 :
    else:
        for columna in range (6,9,1):
            if periodoHoraT[columna][1]:
                

                if registro.time() >= periodoHoraT[columna][1] and registro.time() <= periodoHoraT[columna][2]:
                    
                    return periodoHoraT[columna][0]
           
            if periodoHoraT[columna][3]:
                

                if registro.time() >= periodoHoraT[columna][3] and registro.time() <= periodoHoraT[columna][4]:
                    
                    return periodoHoraT[columna][0]
            
            if periodoHoraT[columna][5]:
              

                if registro.time() >= periodoHoraT[columna][5] and registro.time() <= periodoHoraT[columna][6]:
                    
                    return periodoHoraT[columna][0]
def toTime(T1):
     for columna in range(0,len(T1),1):
            
        for element in range (1,len(T1[columna])):
           
            if type(T1[columna] [element]) == str :
                

                T1[columna] [element]=dt.datetime.strptime(T1[columna][ element],'%H:%M').time()

             

       

    
    
                
    
 



        


   