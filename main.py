# Main.py Este modulo servira como login
#!/usr/local/python

from app.database.conexion import Conexion
from app.database.crear_database import CrearDB
from tkinter import *
from tkinter import messagebox, ttk
from app.ventanas import *
from app.herramientas.sniffer import directorios
import shutil
import os

class Login(BaseWindow):
    def __init__(self):
        super().__init__(titulo='G-RAC Login')

        self.user = StringVar()
        self.passwd = StringVar()
        self.count = 0

        Label(self.window, text='Login', fg=self.color_letra,
              bg=self.color_fondo).place(x=140, y=10)

        Label(self.window, text='Usuario',
              fg=self.color_letra, bg=self.color_fondo).place(x=20, y=40)
        self.entry = Entry(self.window, textvariable=self.user)
        self.entry.focus()
        self.entry.place(x=105, y=40)

        Label(self.window, text='Contraseña',
              fg=self.color_letra, bg=self.color_fondo).place(x=20, y=80)
        Entry(self.window, show='*', textvariable=self.passwd).place(x=105, y=80)

        self.message = Label(self.window, text=' ', fg='red', bg=self.color_fondo)
        self.message.place(x=100, y=110)

        self.bt_1 = Button(self.window, text='Entrar', command=self.enter, width=20)
        self.bt_1.place(x=65, y=135)

        self.window.geometry("300x170")
        self.window.mainloop()

    def enter(self):
        if self.validate():
            print('entramos a la app')
            self.window.destroy()
            print('Se logeo correctamente')
            #Registro()
            SeleccionarProyecto()
        else:
            self.count += 1
            self.message['text'] = f'Contraseña erronea'
            messagebox.showerror('Error', f'Contraseña ingresada {self.count} veces incorrectamente') if self.count % 5 == 0 else ' '

    def validate(self):
        query = 'select * from users where user=? AND passwd=?'
        parameters = (self.user.get(), self.passwd.get())
        user = Conexion().run_query(query, parameters)
        val = [member for member in user]
        return True if val else False

class SeleccionarProyecto(BaseWindow):
    def __init__(self):
        super().__init__(titulo='Proyectos')

        self.tree_proyectos = ttk.Treeview(self.window, height=5, columns=(0,))
        self.tree_proyectos.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
        self.tree_proyectos.heading('#0', text='ID', anchor=CENTER)
        self.tree_proyectos.heading('#1', text='Proyecto', anchor=CENTER)
        self.tree_proyectos.column('#0', width=40)
        self.tree_proyectos.column('#1', width=350)
        self.tree_proyectos.bind("<Double-1>", self.dc_proyecto)

        self.llenar_tree_proyectos()

        self.btn_crear = Button(self.window, text='Crear Proyecto', command=self.crear_proyecto)
        self.btn_crear.grid(row=1, column=0, sticky= W+E, padx=10, pady=5)

        self.btn_crear = Button(self.window, text='Borrar Proyecto', command=self.borrar_proyecto)
        self.btn_crear.grid(row=1, column=1, sticky=W+E, padx=10, pady=5)

    def llenar_tree_proyectos(self):
        files = directorios('app/proyectos_database', delimiter_1='db')
        print(files)
        elements = self.tree_proyectos.get_children()
        for element in elements:
            self.tree_proyectos.delete(element)
        for num,file in enumerate(files):
            self.tree_proyectos.insert('', 0, text=num+1, values=(file.strip('.db'),))

    def dc_proyecto(self, event):
        proyecto = self.tree_proyectos.item(self.tree_proyectos.selection())['values'][0]
        print(proyecto)
        self.window.destroy()
        Registro(database_proyec=f'{proyecto}.db')

    def crear_proyecto(self):
        print('Creando proyecto')

        self.window_crear_proyecto = Toplevel()
        self.window_crear_proyecto.title('Crear nuevo proyecto')
        self.window_crear_proyecto.config(background= self.color_excepcion)

        self.nuevo_proyecto = StringVar()

        Label(self.window_crear_proyecto, text='Nombre del proyecto', bg=self.color_excepcion, fg=self.color_letra).grid(row=0, column=0, pady=5, padx=10)
        Entry(self.window_crear_proyecto, textvariable=self.nuevo_proyecto).grid(row=0, column=1, pady=5, padx=10)

        self.btn_nombre_proyecto = Button(self.window_crear_proyecto, text='Crear proyecto', command=self.crear_db_de_proyecto)
        self.btn_nombre_proyecto.grid(row=1, column=0, padx=10, pady=5, sticky=W+E, columnspan=2)

    def crear_db_de_proyecto(self):
        #print(f'creando a traves de un metodo, db: {self.nuevo_proyecto.get()}')
        try:
            CrearDB(db_name_called= self.nuevo_proyecto.get())
        except ValueError as ex:
            messagebox.showwarning('Error en la creacion de la db',ex)
        self.window_crear_proyecto.destroy()
        self.llenar_tree_proyectos()

    def borrar_proyecto(self):
        try:
            nombre_proyecto = self.tree_proyectos.item(self.tree_proyectos.selection())['values'][0]
        except IndexError as ex:
            messagebox.showwarning('Error en seleccion','Debe seleccionar un proyecto')
            return
        print('todo ok para borrar')
        print(nombre_proyecto)
        os.remove(f'app/proyectos_database/{nombre_proyecto}.db')
        shutil.rmtree(f"frame_image/{nombre_proyecto}")
        self.llenar_tree_proyectos()

if __name__ == '__main__':
    window = Login()
