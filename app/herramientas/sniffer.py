# ver que archivos hay en el direcotrio actual

from os import scandir

__all__ = ['directorios']

def directorios(path):
    return [obj.name for obj in scandir(path) if obj.is_file() if (obj.name.endswith('.jpg') or obj.name.endswith('.png'))]

if __name__ == '__main__':
    directories = directorios('../frame_image')
    print(directories)