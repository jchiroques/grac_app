# Este Módulo sirve para definir el formato de las actividades
from string import ascii_letters

__all__ = ['ValidType','Actividad']

class ValidType:
    def __init__(self,type_):
        self._type = type_

    def __set_name__(self, owner, name):
        self._prop_name = name

    def __set__(self, instance, value):
        if not isinstance(value,self._type):
            raise TypeError(f'{value} debe ser {self._type}')
        if self._type is int and value<0:
            raise ValueError(f'{value} debe ser mayor que 0')
        if self._type is str:
            validate = all([letter in ascii_letters+' ' for letter in value])
            if not validate:
                raise TypeError(f'{value} debe contener solo caracteres alfanumericos')
        instance.__dict__[self._prop_name] = value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return instance.__dict__.get(self._prop_name,None)

class Actividad:
    semana = ValidType(int)
    miembro = ValidType(str)

    def __init__(self,miembro,semana,exp,actividad):
        self.semana = semana
        self.miembro = miembro
        self.exp = exp
        self.actividad = actividad

