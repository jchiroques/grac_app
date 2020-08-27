# Ventana de registro de app
# En este modulo contruiremos la ventana para el registro de actividades

from tkinter import *
from app.objetos import *
from tkinter.ttk import Style
from tkinter import messagebox, filedialog, ttk
from app.database.conexion import Conexion
import configparser
from collections import defaultdict
from PIL import ImageTk, Image
from app.herramientas import *

__all__ = ['BaseWindow', 'Registro', 'Config', 'ConfigType', 'SectionType']

class SectionType(type):
    def __new__(cls, name, bases, cls_dict, section_name, items_dict):
        cls_dict['__doc__'] = f'Configs for {section_name} section'
        cls_dict['section_name']= section_name
        for key,value in items_dict.items():
            #print(f'key: {key}\nvalue: {value}\n')
            cls_dict[key] = value
        return super().__new__(cls, name, bases, cls_dict)

    def __iter__(self):
        yield from vars(self).items()

class ConfigType(type):
    def __new__(cls, name, bases, cls_dict, env):
        """
        env: str
            The enviorement we are loading config
        """
        cls_dict['__doc__']=f'Configurations for {env}'
        cls_dict['env']=env
        config = configparser.ConfigParser()
        file_name = f'../configuracion/{env}.ini' if __name__ == '__main__' else f'app/configuracion/{env}.ini'
        config.read(file_name)
        for section_name in config.sections():
            #print(f'section_name: {section_name}')
            class_name = section_name.capitalize()
            class_attr_name = section_name.casefold()
            section_items = config[section_name]
            bases = (object,)
            section_cls_dict = {}
            section = SectionType(
                class_name, bases, section_cls_dict, section_name=section_name, items_dict=section_items
            )
            cls_dict[class_attr_name] = section
        return super().__new__(cls,name,bases,cls_dict)

class Config(metaclass= ConfigType, env='config'):
    pass

class BaseWindow():
    color_fondo = f'#{Config.config.color_de_fondo}'
    color_letra = f'#{Config.config.color_de_letra}'
    color_excepcion = f'#{Config.config.color_de_excepcion}'
    nombre_del_grupo = f'{Config.grupo.nombre_del_grupo}'
    list_grados = [grado[1] for grado in Config.grados if grado[0].startswith('g')]
    lista_casa_estudios = [uni[1] for uni in Config.estudios if uni[0].startswith('c')]

    def __init__(self, titulo='Titulo Genérico'):
        self.window = Tk()
        self.window.title(titulo)
        self.window.configure(background=BaseWindow.color_fondo)


class Registro(BaseWindow):
    def __init__(self, database_proyec = 'proyecto_1.db'):
        super().__init__(titulo=f'{self.nombre_del_grupo}')
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill='both', expand='yes')

        self.database_proyec = database_proyec
        self.folder_imagenes = database_proyec.strip('.db')

        self.s = Style()
        self.s.configure('My.TFrame', background=self.color_fondo, foreground=self.color_letra)

        self.mostrar_barra_menu()
        self.pes_mostrar_actividades()
        self.pes_guardar_actividades()
        self.pes_registrar_miembros()
        self.pes_imagenes_final()

        self.window.mainloop()

    def mostrar_barra_menu(self):
        self.barra_menu = Menu(self.window)
        self.menu_exportar = Menu(self.barra_menu)

        self.menu_exportar.add_command(label='Exportar actividades', command=self.exportar_actividades)
        self.menu_exportar.add_command(label='Exportar miembros', command=self.exportar_miembros)

        self.barra_menu.add_cascade(label='Exportar', menu= self.menu_exportar)

        self.window.config(menu=self.barra_menu)

    def exportar_actividades(self):
        print('Exportando actividades')
        conn = Conexion(self.database_proyec)
        sql = 'select * from activities'
        actividades = conn.run_query(sql)
        with filedialog.asksaveasfile(title='Guardar como',defaultextension=".csv",filetypes=(("Archivo csv","*.csv"),("Todos Archivos","*.*"))) as f:
            f.write('Semana,Actividad,Responsable,Exp\n')
            for activity in actividades:
                activity = [(act.strip("\n") if isinstance(act,str) else act) for act in activity]
                activity = [(''.join(act.split(",")) if isinstance(act,str) else act) for act in activity]
                activity = [f'{act}' for act in activity]
                f.write(','.join(activity[1:])+'\n')
        messagebox.showinfo('Guardado','Actividades guardadas')

    def exportar_miembros(self):
        print('Exportar miembros')
        conn = Conexion(self.database_proyec)
        sql = 'select * from miembros'
        miembros = conn.run_query(sql)
        with filedialog.asksaveasfile(title='Guardar como',defaultextension=".csv",filetypes=(("Archivo csv","*.csv"),("Todos Archivos","*.*"))) as f:
            f.write('Miembro,Edad,Ciclo o Grado,Casa de estudios\n')
            for miembro in miembros:
                miembro = [(m.strip('\n') if isinstance(m,str) else m) for m in miembro]
                miembro = [f'{mie}' for mie in miembro]
                f.write(','.join(miembro[1:])+'\n')
        messagebox.showinfo('Guardado','Integrantes guardados')

    def pes_mostrar_actividades(self):
        self.pes_0 = ttk.Frame(self.notebook,style='My.TFrame')
        self.notebook.add(self.pes_0,text='Actividades')
        self.ver_semana = StringVar()
        self.ver_semana.set(1)

        self.label_frame_0 = LabelFrame(self.pes_0,text=f'Actividades de {Config.grupo.nombre_del_grupo}',
                                        fg=self.color_letra,bg=self.color_fondo)
        self.label_frame_0.grid(row=0,column=0,padx=10,pady=10)

        Label(self.label_frame_0,text='Semana: ',bg=self.color_fondo,
              fg=self.color_letra).grid(row=0,column=0,padx=10,pady=5)
        Entry(self.label_frame_0,textvariable=self.ver_semana,width=40).grid(row=0,column=1,padx=10,pady=5)
        Button(self.label_frame_0,text='Buscar',width=30,command=self.llenar_mostrador_actividades).grid(row=0,column=2,padx=10,pady=5)

        self.message_mostrar_actividad = Label(self.label_frame_0,text='Actividades',bg=self.color_fondo,fg=self.color_letra)
        self.message_mostrar_actividad.grid(row=1,column=0,columnspan=3,padx=10,pady=5)

        self.tree_actividad_miembro = ttk.Treeview(self.label_frame_0, height=7, columns=(0,))
        self.tree_actividad_miembro.grid(row=2, column=0, columnspan=3, padx=10, pady=5)
        self.tree_actividad_miembro.heading('#0', text='Nombre', anchor=CENTER)
        self.tree_actividad_miembro.heading('#1', text='Actividad (Claro: si exp., oscuro: no exp.)', anchor=CENTER)
        self.tree_actividad_miembro.column('#0', width=300)
        self.tree_actividad_miembro.column('#1', width=430)
        self.tree_actividad_miembro.tag_configure('si', background='#CCFFCC')
        self.tree_actividad_miembro.tag_configure('no', background='#006666', foreground='#FFFFFF')

        Label(self.label_frame_0, text='Resumen de exposiciones por semana', bg=self.color_fondo, fg=self.color_letra).grid(row=3, column=0, columnspan=3, sticky=W+E)

        self.mostrar_informacion_de_exposiciones()

    def mostrar_informacion_de_exposiciones(self):
        sem = defaultdict(dict)
        for miembro in Conexion(self.database_proyec).run_query('select * from activities'):
            sem[miembro[3]].update({miembro[1]: miembro[4]})
        sem_miembros = dict(sem)
        semanas = [sem[0] for sem in Conexion(self.database_proyec).run_query('select distinct semana from activities')]
        expos = defaultdict(list)
        for miembro,exposiciones in sem_miembros.items():
            for semana in semanas:
                expos[miembro] += ['x' if exposiciones.get(semana, 'no') == 'si' else ' ']

        columns = tuple(range(0,len(semanas)))
        ancho = 550
        width = int(ancho/(len(semanas)+1))
        self.tree_exposicion = ttk.Treeview(self.label_frame_0, height=7, columns=columns)
        self.tree_exposicion.grid(row=4, column=0, columnspan=3, padx=10, pady=5)
        self.tree_exposicion.heading('#0', text=f'Nombre', anchor=CENTER)
        self.tree_exposicion.column('#0', width=800-ancho)

        for column in range(1,len(semanas)+1):
            self.tree_exposicion.heading(f'#{column}', text=f'{column}', anchor=CENTER)
            self.tree_exposicion.column(f'#{column}', width=width)

        self.tree_exposicion.tag_configure('par', background='#CCFFCC')
        self.tree_exposicion.tag_configure('impar', background='#006666', foreground='#FFFFFF')

        elements = self.tree_exposicion.get_children()
        for element in elements:
            self.tree_exposicion.delete(element)
        count = 0
        for miembro, aspas in expos.items():
            color = 'par' if count% 2 == 0 else 'impar'
            count += 1
            self.tree_exposicion.insert('',0,text=miembro,values=tuple(aspas),tags=(color,))

        self.message_mostrar_actividad['text']='Actividad encontrada'

    def llenar_mostrador_actividades(self):
        elements = self.tree_actividad_miembro.get_children()
        for element in elements:
            self.tree_actividad_miembro.delete(element)
        conn = Conexion(self.database_proyec)
        query = 'select * from activities where semana=?'
        try:
            parameters = (int(self.ver_semana.get()),)
            actividades_a_mostrar = conn.run_query(query,parameters)
            actividades_a_mostrar = [v for v in actividades_a_mostrar]
            for ac_mostrar in actividades_a_mostrar:
                exp_temp = ac_mostrar[4]
                self.tree_actividad_miembro.insert('',0,text=ac_mostrar[3],values=(ac_mostrar[2],ac_mostrar[3]),tags=(exp_temp,))
            self.message_mostrar_actividad['text']='Actividad encontrada' if actividades_a_mostrar else "Actividad no encontrada"
        except ValueError as ex:
            self.message_mostrar_actividad['text']='La semana debe ser un numero entero'

    def pes_imagenes_final(self):
        self.pes_img = ttk.Frame(self.notebook, style='My.TFrame')
        self.notebook.add(self.pes_img,text='Imagenes')

        self.label_imagenes = LabelFrame(self.pes_img,text='Proyecto',fg=self.color_letra,bg=self.color_fondo)
        self.label_imagenes.grid(row=0, column=0, padx=10, pady=5,sticky=W+E, rowspan=2)

        self.imagen = 'temp'
        self.imagen_proyecto = 'temp_2'

        self.tree_imagenes = ttk.Treeview(self.pes_img, height=19, columns=(0,))
        self.tree_imagenes.grid(row=0,column=1,padx=10, pady=10)

        self.tree_imagenes.heading('#0', text=f'ID', anchor=CENTER)
        self.tree_imagenes.heading('#1', text=f'Imagen', anchor=CENTER)
        self.tree_imagenes.column('#0', width=40)
        self.tree_imagenes.column('#1', width=250)
        self.tree_imagenes.bind("<Double-1>",self.presionar_doble_click)

        self.llenar_tabla_imagenes()

        self.message_imagen = Label(self.pes_img, text='Listo para mostrar', fg=self.color_letra, bg=self.color_fondo)
        self.message_imagen.grid(row=1, column=1, padx=10, pady=5)

    def llenar_tabla_imagenes(self):
        directories = directorios(f'frame_image/{self.folder_imagenes}')
        elements = self.tree_imagenes.get_children()
        for element in elements:
            self.tree_imagenes.delete(element)
        for numero,directory in enumerate(directories):
            self.tree_imagenes.insert('',0,text=numero+1,values=(directory,))

    def presionar_doble_click(self, event):
        self.message_imagen['text']=''
        try:
            int(self.tree_imagenes.item(self.tree_imagenes.selection())['text'])
            print(self.tree_imagenes.item((self.tree_imagenes.selection())))
        except ValueError as e:
            self.message_imagen['text'] = 'Por favor selecciona una imagen'
            return
        imagen_mostrando = self.tree_imagenes.item(self.tree_imagenes.selection())['values'][0]

        # Actualizando imagen
        path_imagen = f'frame_image/{self.folder_imagenes}/{imagen_mostrando}'
        del self.imagen
        del self.imagen_proyecto
        self.imagen = ImageTk.PhotoImage(Image.open(path_imagen).resize((450,450), Image.ANTIALIAS))
        self.imagen_proyecto = Label(self.label_imagenes, image=self.imagen)
        self.imagen_proyecto.grid(row=0, column=0)

        self.message_imagen['text']=f'Mostrando {imagen_mostrando}'

    def pes_guardar_actividades(self):
        self.pes_1 = ttk.Frame(self.notebook,style='My.TFrame')
        self.notebook.add(self.pes_1,text='Database')
        self.semana = StringVar()
        self.semana.set(1)

        self.label_frame_1 = LabelFrame(self.pes_1,text=f'Registrar Actividades de {Config.grupo.nombre_del_grupo}',
                                        fg=self.color_letra,bg=self.color_fondo)
        self.label_frame_1.grid(row=0,column=0,padx=30,pady=10)

        Label(self.label_frame_1,text='Miembro: ',bg=self.color_fondo,
              fg=self.color_letra).grid(row=0,column=0,padx=10,pady=5)
        self.combo_miembros = ttk.Combobox(self.label_frame_1,width=30)
        self.combo_miembros.grid(row=0,column=1,padx=10,pady=5)
        self.llenar_combo_miembros()

        Label(self.label_frame_1,text='Exp: ',bg=self.color_fondo,
              fg=self.color_letra).grid(row=0,column=2,padx=10,pady=5)
        self.combo_exp = ttk.Combobox(self.label_frame_1,width=5)
        self.combo_exp.grid(row=0,column=3,padx=10,pady=5)
        self.combo_exp['values']=['si','no']
        self.combo_exp.current(0)

        Label(self.label_frame_1,text='Semana: ',bg=self.color_fondo,
              fg=self.color_letra).grid(row=0,column=4,padx=10,pady=5)
        Entry(self.label_frame_1,textvariable=self.semana,width=5).grid(row=0,column=5,padx=5,pady=5)

        self.text = Text(self.label_frame_1,width=85,height=3,wrap=WORD)
        self.text.grid(row=1,column=0,padx=10,pady=5,columnspan=6)

        self.guardar_act = Button(self.label_frame_1,text='Guardar',command=self.guardar_actividad_de_miembro)
        self.guardar_act.grid(row=2,column=0,padx=10,pady=5,columnspan=2,sticky=W+E)

        self.message_actividad = Label(self.label_frame_1,text=f'Actividades de {self.nombre_del_grupo}',
                                       fg=self.color_letra,bg=self.color_fondo)
        self.message_actividad.grid(row=3,column=0,padx=7,pady=5,columnspan=6)

        self.tree_actividad = ttk.Treeview(self.label_frame_1,height=10,columns=(0,1,2))
        self.tree_actividad.grid(row=4,column=0,columnspan=7,padx=10,pady=5)
        self.tree_actividad.heading('#0',text='Nombre',anchor=CENTER)
        self.tree_actividad.heading('#1',text='Exp',anchor=CENTER)
        self.tree_actividad.heading('#2',text='Semana',anchor=CENTER)
        self.tree_actividad.heading('#3',text='Actividad',anchor=CENTER)
        self.tree_actividad.column('#0',width=245)
        self.tree_actividad.column('#1',width=50)
        self.tree_actividad.column('#2',width=70)
        self.tree_actividad.column('#3',width=340)
        self.tree_actividad.tag_configure('si', background='#DFE0E9')
        self.tree_actividad.tag_configure('no', background='#838487', foreground='#FFFFFF')

        Button(self.label_frame_1,text='Editar actividad',command=self.actualizar_actividades_miembros).grid(row=5,column=0,padx=10,pady=5,columnspan=3,sticky=W+E)
        Button(self.label_frame_1,text='Borrar actividad',command=self.eliminar_actividad_de_miembro).grid(row=5,column=3,padx=10,pady=5,columnspan=3,sticky=W+E)

        self.llenar_tabla_actividades_miembros()

    def llenar_combo_miembros(self):
        conn = Conexion(self.database_proyec)
        query = 'select complete_name from miembros'
        miembros_com = conn.run_query(query)
        miembros_com = [m[0] for m in miembros_com]
        self.combo_miembros['values']=miembros_com or 'Vacio'
        self.combo_miembros.current(0)

    def guardar_actividad_de_miembro(self):
        try:
            actividad_ = Actividad(self.combo_miembros.get(),int(self.semana.get()),
                                  self.combo_exp.get(),self.text.get(1.0,END).strip('\n'))
            conn = Conexion(self.database_proyec)
            query = "INSERT INTO activities VALUES(NULL,?,?,?,?)"
            parameters = (actividad_.semana,actividad_.actividad,actividad_.miembro,actividad_.exp)
            conn.run_query(query, parameters)
            self.text.delete(1.0,END)
            self.message_actividad['text']='Actividad guardada'

            pos = (self.len_activities+1) % self.len_miembros
            self.semana.set(int(self.semana.get()) + int(not(bool(pos))))
            self.combo_miembros.current(pos)
            self.llenar_tabla_actividades_miembros()

        except Exception as ex:
            self.message_actividad['text']=ex

    def eliminar_actividad_de_miembro(self):
        try:
            self.tree_actividad.item(self.tree_actividad.selection())['text'][0]
        except IndexError as e:
            self.message_actividad['text'] = 'Por favor selecciona un miembro'
            return
        self.message_actividad['text']=''
        nombre = self.tree_actividad.item(self.tree_actividad.selection())['text']
        exp = self.tree_actividad.item(self.tree_actividad.selection())['values'][0]
        semana = int(self.tree_actividad.item(self.tree_actividad.selection())['values'][1])
        actividad = self.tree_actividad.item(self.tree_actividad.selection())['values'][2]
        conn = Conexion(self.database_proyec)
        query = "DELETE FROM activities WHERE semana=? AND actividad=? AND responsable=? AND exp=?"
        conn.run_query(query,(semana,actividad,nombre,exp))
        self.message_actividad['text'] = f'{actividad} eliminado'

        self.llenar_tabla_actividades_miembros()

    def actualizar_actividades_miembros(self):
        try:
            self.tree_actividad.item(self.tree_actividad.selection())['text'][0]
        except IndexError as e:
            self.message_actividad['text'] = 'Por favor selecciona un miembro'
            return
        self.name_old_actividad = self.tree_actividad.item(self.tree_actividad.selection())['text']
        self.semana_old = int(self.tree_actividad.item(self.tree_actividad.selection())['values'][1])
        self.actividad_old = self.tree_actividad.item(self.tree_actividad.selection())['values'][2]

        self.new_name = StringVar()
        self.new_semana = StringVar()
        self.new_actividad = StringVar()

        self.ventana_actualizar_actividad = Toplevel()
        self.ventana_actualizar_actividad.title('Actualizanco actividades')
        self.ventana_actualizar_actividad.config(background=self.color_excepcion)

        Label(self.ventana_actualizar_actividad,text='Actualizar Actividad',fg=self.color_letra,bg=self.color_excepcion).grid(row=0,column=0,columnspan=2,padx=10,pady=5)

        #Actualizar nombre
        self.new_name.set(self.name_old_actividad)
        Label(self.ventana_actualizar_actividad, text='Nombre: ',fg=self.color_letra,bg=self.color_excepcion).grid(row=1, column=0, padx=10, pady=5)
        Entry(self.ventana_actualizar_actividad, textvariable=self.new_name,width=30).grid(row=1, column=1, padx=10, pady=5)

        # Actualizar exp
        Label(self.ventana_actualizar_actividad, text='Exp: ',fg=self.color_letra,bg=self.color_excepcion).grid(row=2, column=0, padx=10, pady=5)
        self.combo_new_exp = ttk.Combobox(self.ventana_actualizar_actividad,values=('si','no'), width=29)
        self.combo_new_exp.grid(row=2, column=1, padx=10, pady=5)
        self.combo_new_exp.current(0)

        #Actualizar semana
        self.new_semana.set(self.semana_old)
        Label(self.ventana_actualizar_actividad,text='Semana:', fg=self.color_letra, bg=self.color_excepcion).grid(row=3, column=0, padx=10, pady=5)
        Entry(self.ventana_actualizar_actividad,textvariable=self.new_semana, width=30).grid(row=3, column=1, padx=10, pady=5)

        #Actualizar Actividad
        self.new_actividad.set(self.actividad_old)
        Label(self.ventana_actualizar_actividad,text='Actividad:',fg=self.color_letra,bg=self.color_excepcion).grid(row=4, column=0, padx=10, pady=5)
        self.text_actualizar = Text(self.ventana_actualizar_actividad,height=4,width=40, wrap=WORD)
        self.text_actualizar.insert(INSERT,self.new_actividad.get())
        self.text_actualizar.grid(row=5,column=0, padx=10, pady=5, columnspan=2)

        Button(self.ventana_actualizar_actividad, text='Actualizar Actividad', command=self.actualizar_tabla_actividades).grid(row=6, column=0, padx=10, pady=5, columnspan=2, sticky=W+E)

    def actualizar_tabla_actividades(self):
        print(self.new_name.get(),self.combo_new_exp.get(),self.new_semana.get(),self.text_actualizar.get(1.0,END))
        try:
            actividad = Actividad(self.new_name.get(),int(self.new_semana.get()),self.combo_new_exp.get(),self.text_actualizar.get(1.0,END))
        except Exception as ex:
            messagebox.showwarning('Ocurrio un error',ex)
            return
        conn = Conexion(self.database_proyec)
        query = "UPDATE activities SET semana=?, actividad=?, responsable=?, exp=? WHERE semana=? AND actividad=? AND responsable=?"
        parameters = (actividad.semana, actividad.actividad, actividad.miembro, actividad.exp, self.semana_old, self.actividad_old, self.name_old_actividad)
        conn.run_query(query,parameters)
        messagebox.showinfo('Actualizado',f'Actualizado {actividad.miembro} exitosamente.')
        self.message_actividad['text']=f'Actualizado {actividad.miembro} exitosamente.'

        self.llenar_tabla_actividades_miembros()
        self.ventana_actualizar_actividad.destroy()

    def llenar_tabla_actividades_miembros(self):
        elements = self.tree_actividad.get_children()
        for element in elements:
            self.tree_actividad.delete(element)
        conn = Conexion(self.database_proyec)
        query = 'select * from activities'
        activities_ = [act for act in conn.run_query(query)]
        self.len_activities = len(activities_)
        for act in activities_:
            color = 'si' if int(act[1])%2==0 else 'no'
            self.tree_actividad.insert('',0,text=act[3],values=(act[4],act[1],act[2]),tags=(color,))

        self.mostrar_informacion_de_exposiciones()

    def pes_registrar_miembros(self):
        self.pes_2 = ttk.Frame(self.notebook,style='My.TFrame')
        self.notebook.add(self.pes_2,text='Miembros')
        self.name = StringVar()
        self.edad = StringVar()
        self.edad.set(20)

        self.label_frame_2 = LabelFrame(self.pes_2,text=f'Miembros de {Config.grupo.nombre_del_grupo}',
                                        fg=self.color_letra,bg=self.color_fondo)
        self.label_frame_2.grid(row=0,column=0,padx=20,pady=20)

        Label(self.label_frame_2,text='Nombre: ',bg=self.color_fondo,
              fg=self.color_letra).grid(row=0,column=0,padx=10,pady=5)
        Entry(self.label_frame_2,textvariable=self.name,width=30).grid(row=0,column=1)

        Label(self.label_frame_2,text='Edad: ',bg=self.color_fondo,
              fg=self.color_letra).grid(row=0,column=2,padx=10,pady=5)
        Entry(self.label_frame_2,textvariable=self.edad,width=4).grid(row=0,column=3)

        Label(self.label_frame_2,text='Ciclo o grado: ',bg=self.color_fondo,
              fg=self.color_letra).grid(row=0,column=4,padx=10,pady=5)
        self.combo_grado = ttk.Combobox(self.label_frame_2,width=15)
        self.combo_grado.grid(row=0,column=5,padx=10,pady=5)
        self.combo_grado['values'] = [f'Ciclo {i}' for i in range(1,11)] + self.list_grados
        self.combo_grado.current(9)

        Button(self.label_frame_2,text='Guardar Miembros',
               command=self.guardar_miembro).grid(row=1,column=0,padx=10,pady=5,columnspan=2,sticky=W+E)

        Label(self.label_frame_2,text='Casa de Estudios:',fg=self.color_letra,bg=self.color_fondo).grid(row=1,column=2,columnspan=2,padx=5,pady=5)
        self.combo_casa_estudios = ttk.Combobox(self.label_frame_2,width=15)
        self.combo_casa_estudios.grid(row=1,column=4,columnspan=2,padx=10,pady=5,sticky=W+E)
        self.combo_casa_estudios['values']= self.lista_casa_estudios
        self.combo_casa_estudios.current(0)

        self.message_miembro = Label(self.label_frame_2,text=f'Listo para ingresar Datos del grupo {self.nombre_del_grupo}',
                                     fg=self.color_letra,bg=self.color_fondo)
        self.message_miembro.grid(row=2,column=0,columnspan=7,sticky=W+E)

        self.tree_miembro = ttk.Treeview(self.label_frame_2,height=12,columns=(0,1,2))
        self.tree_miembro.grid(row=3,column=0,columnspan=7,padx=10,pady=5)
        self.tree_miembro.heading('#0',text='Nombre',anchor=CENTER)
        self.tree_miembro.heading('#1',text='Edad',anchor=CENTER)
        self.tree_miembro.heading('#2',text='Grado',anchor=CENTER)
        self.tree_miembro.heading('#3',text='Casa de Estudios',anchor=CENTER)
        self.tree_miembro.column('#0',width=300)
        self.tree_miembro.column('#1',width=50)
        self.tree_miembro.column('#2',width=100)
        self.tree_miembro.column('#3',width=260)

        Button(self.label_frame_2,text='Editar',command=self.actualizar_miembro).grid(row=4,column=0,padx=10,pady=5,columnspan=3,sticky=W+E)
        Button(self.label_frame_2,text='Borrar',command=self.eliminar_miembro).grid(row=4,column=4,padx=10,pady=5,columnspan=3,sticky=W+E)

        self.llenar_tabla_miembros()

    def llenar_tabla_miembros(self):
        elements = self.tree_miembro.get_children()
        for element in elements:
            self.tree_miembro.delete(element)
        conn = Conexion(self.database_proyec)
        query = 'select * from miembros'
        miembros = conn.run_query(query)
        miembros = [ miem for miem in miembros]
        self.len_miembros = len(miembros)
        for miembro in miembros:
            self.tree_miembro.insert('',0,
                    text=miembro[1],values=(miembro[2],miembro[3],miembro[4]))
        self.llenar_combo_miembros()

    def guardar_miembro(self):
        try:
            miembro = Miembro(self.name.get(),int(self.edad.get()),self.combo_grado.get(),self.combo_casa_estudios.get())
            conn = Conexion(self.database_proyec)
            query = "INSERT INTO miembros VALUES(NULL,?,?,?,?)"
            parameters = (miembro.name,miembro.edad,miembro.grado,miembro.casa_estudios)
            conn.run_query(query, parameters)
            self.name = ''
            self.edad = ''
            self.combo_grado.current(9)

            self.llenar_tabla_miembros()
        except Exception as ex:
            self.message_miembro['text'] = ex

    def eliminar_miembro(self):
        try:
            self.tree_miembro.item(self.tree_miembro.selection())['text'][0]
        except IndexError as e:
            self.message_miembro['text'] = 'Por favor selecciona un miembro'
            return
        self.message_miembro['text']=''
        name = self.tree_miembro.item(self.tree_miembro.selection())['text']
        edad = self.tree_miembro.item(self.tree_miembro.selection())['values'][0]
        grado = self.tree_miembro.item(self.tree_miembro.selection())['values'][1]
        conn = Conexion(self.database_proyec)
        query = "DELETE FROM miembros WHERE complete_name=? AND edad=? AND grado_ciclo=?"
        conn.run_query(query,(name,edad,grado))
        self.message_miembro['text'] = f'{name} eliminado'

        self.llenar_tabla_miembros()

    def actualizar_miembro(self):
        try:
            self.tree_miembro.item(self.tree_miembro.selection())['text'][0]
        except IndexError as e:
            self.message_miembro['text'] = 'Por favor selecciona un miembro'
            return
        self.name_old = self.tree_miembro.item(self.tree_miembro.selection())['text']
        self.edad_old = self.tree_miembro.item(self.tree_miembro.selection())['values'][0]
        self.grado_old = self.tree_miembro.item(self.tree_miembro.selection())['values'][1]
        print(self.name_old,self.edad_old,self.grado_old)
        self.nombre_miembro = StringVar()
        self.edad_miembro = IntVar()

        self.editar_miembro = Toplevel()
        self.editar_miembro.title('Editar miembro')
        self.editar_miembro.config(background=self.color_excepcion)

        Label(self.editar_miembro,text='Editar Miembro', fg=self.color_letra, bg=self.color_excepcion).grid(row=0, column=0, columnspan=2, padx=10, pady=5)

        #Modificar nombre
        self.nombre_miembro.set(self.name_old)
        Label(self.editar_miembro,text='Nombre:',fg=self.color_letra,
              bg=self.color_excepcion).grid(row=1,column=0,padx=10,pady=5)
        Entry(self.editar_miembro,textvariable=self.nombre_miembro,width=28).grid(row=1,column=1,padx=10,pady=5)

        #Modificar edad
        self.edad_miembro.set(self.edad_old)
        Label(self.editar_miembro,text='Edad:',fg=self.color_letra,
              bg=self.color_excepcion).grid(row=2,column=0,padx=10,pady=5)
        Entry(self.editar_miembro,textvariable=self.edad_miembro,
              width=28).grid(row=2,column=1,padx=10,pady=5)

        #Modificar grado
        Label(self.editar_miembro, text='Grado:', fg=self.color_letra,
              bg=self.color_excepcion).grid(row=3, column=0, padx=10, pady=5)

        self.editar_combo_miembro = ttk.Combobox(self.editar_miembro,values=self.list_grados,width=27)
        self.editar_combo_miembro.grid(row=3,column=1,padx=10,pady=5)
        self.editar_combo_miembro.current(0)

        #Modificar Casa de estudios
        Label(self.editar_miembro, text='Casa de Estudios:', fg=self.color_letra,
              bg=self.color_excepcion).grid(row=4, column=0, padx=10, pady=5)

        self.editar_combo_estudios = ttk.Combobox(self.editar_miembro,values=self.lista_casa_estudios, width=27)
        self.editar_combo_estudios.grid(row=4, column=1, padx=10, pady=5)
        self.editar_combo_estudios.current(0)

        Button(self.editar_miembro,text='Actualizar miembro',command=self.actualizar_bd_miembro).grid(row=5,
                                column=0, columnspan=2,sticky=W+E, padx=10, pady=5)

    def actualizar_bd_miembro(self):
        try:
            miembro = Miembro(self.nombre_miembro.get(), int(self.edad_miembro.get()), self.editar_combo_miembro.get(), self.editar_combo_estudios.get())
        except Exception as ex:
            messagebox.showwarning('Error encontrado',ex)
            return
        conn = Conexion(self.database_proyec)
        query = "UPDATE miembros SET complete_name=?, edad=?, grado_ciclo=?, casa_estudios=? WHERE complete_name=? AND edad=? AND grado_ciclo=?"
        parameters = (self.nombre_miembro.get(),self.edad_miembro.get(),self.editar_combo_miembro.get(),self.editar_combo_estudios.get(), self.name_old, self.edad_old, self.grado_old)
        conn.run_query(query,parameters)
        messagebox.showinfo('Actualziado',f'Actualizado con exito {self.nombre_miembro.get()}')

        self.editar_miembro.destroy()
        self.llenar_tabla_miembros()

if __name__ == '__main__':
    reg = Registro()


