import os
from typing import Union
from conf import type_file_IMG, photo_files, video_files, type_file_VID
from base.basicProcess import basicDataError


def get_name(file_name) -> Union[bool, str]:
    """
    Получает только имя, без расширения.
    """
    name = os.path.splitext(file_name)[0]
    if len(name) == 0:
        return False
    else:
        return name


def get_extension(file_name) -> Union[bool, str]:
    """
    Получает только расширение с точкой, без имени - .JPG
    """
    extension = os.path.splitext(file_name)[1]
    if len(extension) == 0:
        return False
    else:
        return extension


def get_location_file(file_name, location) -> str:
    """
    Получает полный путь до файла.
    """
    location_file = os.path.join(location, file_name)
    return location_file


def get_type_file(file_name) -> str:
    """
    Получает тип файла, возвращает 'IMG'/'VID'
    """
    if get_extension(file_name).upper()[1:] in photo_files:
        type_file = type_file_IMG
        return type_file
    elif get_extension(file_name).upper()[1:] in video_files:
        type_file = type_file_VID
        return type_file
    else:
        raise basicDataError(f'The file type is not defined! --> {file_name}')


def get_full_basic_data(file_name, location) -> dict:
    """
    Получает все базовые данные из функций, описанных выше.
    """
    basic_data = {
        "full_name": file_name,
        "name": get_name(file_name),
        "extension": get_extension(file_name),
        "type_file": get_type_file(file_name),
        "location_file": get_location_file(file_name, location)
    }
    return basic_data