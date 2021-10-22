from tabulate import tabulate
def showTarifas(tarifas) :
    
    for diccionario in tarifas:

        tabla=[]
        print('***************************************************************')
        print('\n')
        print('***************************************************************')
        print('===============================================================')
        print(diccionario['description'])
        print("")
        print('===============================================================')
        print('fecha de inicio:       ', diccionario['vigencia']['inicio'])
        print('fecha de finalizacion: ', diccionario['vigencia']['final'])
        print('===============================================================')
         
        for elemento in diccionario['tarifas'].values():

            tabla.append(elemento)
                 
        print(tabulate(tabla))
    return 0
