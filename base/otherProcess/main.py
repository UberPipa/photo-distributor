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
    while c < 50:
        for root, dirs, files in os.walk(source):
            for dir in dirs:
                full_dir_path = os.path.join(root, dir)
                if not os.listdir(full_dir_path):
                    os.rmdir(full_dir_path)
        c += 1


def findAlienFiles(dir) -> None:
    """
    Поиск файлов, которые не числятся в списке и перемещение их в папку Strangers корневой папки:
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

    print('Готово.')


def move_files_to_main_dir(main_dir):
    """
    Перемещает все файлы из подпапок.

    :param main_dir: Путь к основной директории.
    """
    s = 0
    for location, dirs, files in os.walk(main_dir):

        for file in os.listdir(location):
            if check_type_file(file):
                if location == main_dir:
                    continue

                for file in files:
                    file_path = os.path.join(location, file)
                    dest_path = os.path.join(main_dir, file)

                    # Перемещаем только если файл ещё не находится в основной директории
                    if not os.path.exists(dest_path):
                        try:
                            shutil.move(file_path, main_dir)
                        except shutil.Error as e:
                            print(f"Ошибка при перемещении файла '{file}': {e}")

    print('Все файлы перемещены в корневую директорию.')