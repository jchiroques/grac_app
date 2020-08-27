# Este módulo contiene la clase estudiante con sus restricciones.

from string import ascii_letters
from app.herramientas.exceptions import *

__all__ = ['NombreValido', 'EdadValida', 'Miembro']

class NombreValido:
    def __init__(self,min=5):
        self._min = min

    def __set_name__(self, owner, name):
        self._prop_name = name

    def __set__(self, instance, value):
        validate = all([letter in ascii_letters+' ' for letter in value])

        if not (isinstance(value,str) and validate):
            raise AppExcepcion.NFormato.throw('El nombre debe ser un string y solo contener caracteres algabéticos.')
        if len(value)<self._min:
            raise AppExcepcion.NLongitud.throw(f'El nombre debe tener una longitud mayor a {self._min}')
        instance.__dict__[self._prop_name] = value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return instance.__dict__.get(self._prop_name,None)

class EdadValida:
    def __init__(self,min=0,max=80):
        self._min = min
        self._max = max

    def __set_name__(self, owner, name):
        self._prop_name = name

    def __set__(self, instance, value):
        if not isinstance(value,int):
            AppExcepcion.EInvalida.throw('La edad debe ser un valor entero')
        if value < self._min:
            raise AppExcepcion.EInvalida.throw(f'La edad debe ser mayor que {self._min}')
        if value > self._max:
            raise AppExcepcion.EInvalida.throw(f'La edad debe ser menor que {self._max}')
        instance.__dict__[self._prop_name] = value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return instance.__dict__.get(self._prop_name,None)

class Miembro:
    name = NombreValido(5)
    edad = EdadValida(0,80)

    def __init__(self,name,edad,grado,casa_estudios):
        self.name = name
        self.grado = grado
        self.edad = edad
        self.casa_estudios = casa_estudios

