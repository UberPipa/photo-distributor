import os
import shutil

from base.basicProcess.basicCheck import check_type_file


def clearFolderDIr(source) -> None:
    """
    Рекурсивно удаляет пустые директории.
    :param source: Папка для удаления.
    :return:
    """

    c = 0
    while c < 20:
        for root, dirs, files in os.walk(source):
            for dir in dirs:
                full_dir_path = os.path.join(root, dir)
                if not os.listdir(full_dir_path):
                    os.rmdir(full_dir_path)
        c += 1


def findAlienFiles(dir) -> None:
    """
    Поиск файлов, которые не числятся в списке и перемещение их в папку Strangers:
    :param dir: Папка в которой будет происходить данный поиск.
    :return:
    """

    s = 0
    for location, dirs, files in os.walk(dir):
        for file in files:
            if not check_type_file(file):
                old_path = os.path.join(location, file)
                destination_path = os.path.join(dir, "Strangers", file)

                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                shutil.move(str(old_path), str(destination_path))

                s += 1