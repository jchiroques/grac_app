# Encontraremos todas las excepciones a usar

"""
-ExcepcionesApp
    - ErrorEnNombre
        - NombreFormato (100)
        - NombreLongitud (101)
    - TextoLongitud (200)
    - EdadInvalida
"""
import traceback
from datetime import datetime
from enum import Enum,unique

__all__ = ['ExcepcionesApp','ErrorEnNombre','NombreLongitud',
           'NombreFormato','TextoLongitud','AppExcepcion','EdadInvalida']

class ExcepcionesApp(Exception):
    message = 'Mensaje generico de error'

    def __init__(self,*args,customer_message=None):
        super().__init__(*args)
        if args:
            self.message = args[0]
        self.customer_message = customer_message if customer_message is not None else self.message

    @property
    def traceback(self):
        return traceback.TracebackException.from_exception(self).format()

    def log_exception(self):
        exception = {
            "type":type(self).__name__,
            "message":self.customer_message,
            "args":self.args[1:],
            "traceback":list(self.traceback)
        }
        return f'Hora:{datetime.utcnow().isoformat()}',exception

    def __str__(self):
        return f'{self.customer_message}'

class ErrorEnNombre(ExcepcionesApp):
    message = 'Error en el formato del nombre'

class NombreFormato(ErrorEnNombre):
    message = 'El nombre solo debe contener caracteres alfabeticos y ser un String'

class NombreLongitud(ErrorEnNombre):
    message = 'La longitud del nombre es incorrecta'

class TextoLongitud(ExcepcionesApp):
    message = 'Error en la longitud del Texto.'

class EdadInvalida(ExcepcionesApp):
    message = 'Error en el ingreso de la edad'

@unique
class AppExcepcion(Enum):
    NFormato = (100,NombreFormato)
    NLongitud = (101,NombreLongitud)
    TLongitud = (200,TextoLongitud)
    EInvalida = (300,EdadInvalida)

    def __new__(cls,ex_code,ex_class):
        member = object.__new__(cls)

        member._value_ = ex_code
        member.exception = ex_class

        return member

    @property
    def code(self):
        return self.value

    def throw(self,message=None):
        message = message or self.exception.message
        raise self.exception(f'{self.code}-{message}')

if __name__ == '__main__':
    try:
        raise NombreLongitud()
    except ExcepcionesApp as ex:
        print(ex)

    try:
        raise AppExcepcion.NFormato.throw('hola')
    except ExcepcionesApp as ex_1:
        print(ex_1)

