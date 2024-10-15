from conf import photo_files, video_files
from base.basicProcess.basicData import get_name, get_extension


def check_extension_file(file_name) -> bool:
    """
    Функция проверяет, есть ли у файла расширение или нет.
    """
    if get_name(file_name) and get_extension(file_name):
        return True
    else:
        return False


def check_type_file(file_name) -> bool:
    """
    Функция проверяет, есть ли данный файл в установленных списках.
    """
    if check_extension_file(file_name):
        if get_extension(file_name).upper()[1:] in photo_files or get_extension(file_name).upper()[1:] in video_files:
            return True
        else:
            return False
