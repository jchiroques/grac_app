# Este módulo servira para conetarme a la estructura de datos
# hecha en sqlite3

import sqlite3

class Conexion:
    def __init__(self):
        self.db_name = 'app/app.db'

    def run_query(self,query,parameters = ()):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                result = cursor.execute(query,parameters)
                conn.commit()
            print('Conexion Satisfactoria')
            return result
        except:
            print('error al cargar la db')