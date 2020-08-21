

# Main.py Este modulo servira como login

from app.database.conexion import Conexion
from tkinter import *
from tkinter import messagebox
from app.ventanas import *

class Login(BaseWindow):
    def __init__(self):
        super().__init__(titulo='G-RAC Login')

        self.user = StringVar()
        self.passwd = StringVar()
        self.count = 0

        Label(self.window, text='Login', fg=self.color_letra,
              bg=self.color_fondo).place(x=140, y=10)

        Label(self.window,text='Usuario',
              fg=self.color_letra, bg=self.color_fondo).place(x=20, y=40)
        self.entry=Entry(self.window, textvariable=self.user)
        self.entry.focus()
        self.entry.place(x=105, y=40)

        Label(self.window, text='Contraseña',
              fg=self.color_letra, bg=self.color_fondo).place(x=20,y=80)
        Entry(self.window,show='*', textvariable=self.passwd).place(x=105,y=80)

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
            Registro()
        else:
            self.count += 1
            self.message['text'] = f'Contraseña erronea'
            messagebox.showerror('Error',f'Contraseña ingresada {self.count} veces incorrectamente') if self.count % 5 == 0 else ' '

    def validate(self):
        query = 'select * from users where user=? AND passwd=?'
        parameters=(self.user.get(),self.passwd.get())
        user = Conexion().run_query(query,parameters)
        val = [member for member in user]
        return True if val else False

if __name__ == '__main__':
    window = Login()