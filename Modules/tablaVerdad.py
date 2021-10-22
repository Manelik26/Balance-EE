from datetime import datetime
def tablaV(inicio, final):
    
    contador=0
    
    while contador < len(inicio):
        if inicio[contador]:

            if not final[contador]:

                print("Error en periodo horario")
                return 404
        else:
            if final[contador]:
                print("Error en periodo horario")
                return 404
        
        contador +=1
    return 0

def comparadorHora(inicio, final):

    _inicio = datetime.strptime(inicio, '%H:%M')
    _final = datetime.strptime(final, '%H:%M')
    if _inicio >= _final:
        print("La hora final no puede ser menor que la de inicio")
        return 404
    return 0