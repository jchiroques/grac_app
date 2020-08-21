# Este módulo contiene las herramientas para el logueo de la aplicación

import inspect
from functools import wraps
from time import perf_counter

__all__ = ['func_logger','class_logger']

def func_logger(fn):
    @wraps(fn)
    def inner(*args,**kwargs):
        start = perf_counter()
        result = fn(*args,**kwargs)
        elapsed = perf_counter() - start
        print(f'Log: {fn.__qualname__}({args},{kwargs})={result}\
                \ntime:{elapsed}')
        return result
    return inner

def class_logger(cls):
    for name, obj in vars(cls).items():
        if isinstance(obj,staticmethod) or isinstance(obj,classmethod):
            type_ = type(obj)
            original_func = obj.__func__
            print(f'decorating {type_.__name__} method',original_func)
            decorated_func = func_logger(original_func)
            method = type_(decorated_func)
            setattr(cls,name,method)
        elif isinstance(obj,property):
            print(f'decorating property',obj)
            if obj.fget:
                obj = obj.getter(func_logger(obj.fget))
            if obj.fset:
                obj = obj.setter(func_logger(obj.fset))
            if obj.fdel:
                obj = obj.deleter(func_logger(obj.fdel))
            setattr(cls,name,obj)
        elif inspect.isroutine(obj):
            print('decorating routine:',cls,name)
            setattr(cls,name,func_logger(obj))
    return cls

if __name__ == '__main__':
    @class_logger
    class Person:
        def __init__(self,name):
            self.name = name

        def say_hello(self):
            return f'{self.name} says hello'

    p = Person('Jose')
    print(p.say_hello())