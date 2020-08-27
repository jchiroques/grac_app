# ver que archivos hay en el direcotrio actual

from os import scandir

__all__ = ['directorios']

def directorios(path, delimiter_1='.jpg', delimiter_2='.png'):
    return [obj.name for obj in scandir(path) if obj.is_file() if (obj.name.endswith(delimiter_1) or obj.name.endswith(delimiter_2))]

if __name__ == '__main__':
    directories = directorios('../frame_image')
    print(directories)