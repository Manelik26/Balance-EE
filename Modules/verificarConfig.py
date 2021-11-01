
#*******************************************************************************************************************
# Verifica archivo de configuracion de periodos tarifarios 
#*******************************************************************************************************************

import emoji
from datetime import datetime
import Modules.tablaVerdad as TV


def verificar (jsonObject):
    code=0

    try :
        if type(jsonObject)!= list:
            print("Lista de configuracion invalida")
            return 400

        for diccionario in jsonObject:
            
            if type(diccionario) != dict:
                print("Alguno de los archivos de configuracion no es un diccionario")
                return 401   
                
            if diccionario['vigencia']['inicio']==False and diccionario['vigencia']['final']==False:
                print("Error de vigencia")
                return 402 
            
            fechaInicio = datetime.strptime(diccionario['vigencia']['inicio'], '%d/%m/%Y')
            fechaFinal = datetime.strptime(diccionario['vigencia']['final'], '%d/%m/%Y')

            if fechaInicio >= fechaFinal:
                print('Las fechas de vigencia son incorrectas')
                return 403
            
            for horario in diccionario['tarifas'].values():
                
                horaInicio_1 = bool(horario['inicio_1'])
                horaFinal_1 = bool(horario['final_1'])
                horaInicio_2 = bool(horario['inicio_2'])
                horaFinal_2 = bool(horario['final_2'])
                horaInicio_3 = bool(horario['inicio_3'])
                horaFinal_3 = bool(horario['final_3'])
                
                inicio = [ horaInicio_1, horaInicio_2, horaInicio_3]
                final=[horaFinal_1, horaFinal_2, horaFinal_3]
                            
                if TV.tablaV(inicio, final):
                    print("error en periodos horarios")
                    return 404

                if horaInicio_1: 
                    if TV.comparadorHora(horario['inicio_1'], horario['final_1']):
                        print("error en periodos horarios")
                        return 404

                if horaInicio_2: 
                    if TV.comparadorHora(horario['inicio_2'], horario['final_2']):
                        print("error en periodos horarios")
                        return 404
                
                if horaInicio_3: 
                    if TV.comparadorHora(horario['inicio_3'], horario['final_3']):
                        print("error en periodos horarios")
                        return 404
       
            print(emoji.emojize(diccionario['description']+': ''Correcto :thumbs_up:'))

    except:
        print(Exception.with_traceback,"Algo ha ido mal con el archivo de configuracion")
    

            
            


           
        
       
        
    
