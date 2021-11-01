import tkinter as tk
from tkinter import ttk


class Aplicacion():
    def __init__(self):
        raiz = tk.Tk()
        
        raiz.geometry('700x500')
        raiz.title('Balance de energia')


        menu_bar = tk.Menu(raiz)
        cascade = tk.menu(raiz)
        

        menu_bar.add_command(label='Archivo')
        menu_bar.add_command(label='Configuración')
        raiz.config(menu = menu_bar)
       
       

        tk.Button(raiz, text='Salir',  command= raiz.destroy).pack(side='bottom')

        raiz.mainloop()


def main(): 
    mi_app = Aplicacion()

if __name__ == '__main__':
    main()