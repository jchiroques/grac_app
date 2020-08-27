# Crear database

import sqlite3
import os

class ValidateDbName:
    def __set_name__(self, owner, name):
        self._prop_name_1 = name
        print(f'name:{self._prop_name_1}')

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError('El nombre de la base de datos debe ser un string')
        if len(value) == 0:
            raise ValueError('El nombre del string debe ser mayor a 0')
        instance.__dict__[self._prop_name_1] = value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return instance.__dict__.get(self._prop_name_1, None)

class CrearDB:
    db_name = ValidateDbName()

    def __init__(self, db_name_called):
        self.db_name = db_name_called
        print('contructor corriendo')
        print(f'database: {self.db_name}')

        self.crear_data_base()

    def crear_data_base(self):
        with sqlite3.connect(f'app/proyectos_database/{self.db_name}.db') as con:
            print(f'se creo la db: {self.db_name} correctamente')
            cursor = con.cursor()
            cursor.execute("CREATE TABLE activities(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,semana INTEGER NOT NULL, actividad TEXT NOT NULL, responsable TEXT NOT NULL, exp TEXT NOT NULL)")
            con.commit()
            cursor.execute("CREATE TABLE miembros(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, complete_name TEXT NOT NULL, edad	INTEGER NOT NULL, grado_ciclo TEXT NOT NULL, casa_estudios INTEGER)")
            con.commit()
            os.mkdir(f'frame_image/{self.db_name}')