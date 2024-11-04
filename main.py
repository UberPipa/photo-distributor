import os
import sys
import argparse

from base.otherProcess.main import clearFolderDIr, move_files_to_main_dir, findAlienFiles

# Получаем текущую директорию, где находится exe или скрипт
default_directory = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)


from base.example.example import get_info_all_files
from m_inside_meta.imside_meta import insideMeta, insideMeta_lite
from m_rename.rename import rename_for_meta, rename_for_name
from m_report.report import report
from m_sorting.sorting import sorting_for_meta, sorting_for_name


def run() -> None:
    """
    Запускает программу, тт нужно указывать этапы.
    :return:
    """
    parser = argparse.ArgumentParser(description="Консольная утилита для обработки фото и видео файлов")

    # Параметры
    parser.add_argument('-d', '--directory', type=str, default=default_directory, help="Директория для обработки на вход. По умолчанию – директория, где находится .exe файл.")
    parser.add_argument('-i', '--info', action='store_true', help="В указанной директории пробегает по каждому файлу и выводит по нему информацию.")
    parser.add_argument('-r', '--report', action='store_true', help="По указанной директории выводит побробную информацию по всем файлам.")
    parser.add_argument('-sM', '--sorting-meta', action='store_true', help="В указанной директории выполняет сортировку файлов по месяцам и годам исходя из метаданных.")
    parser.add_argument('-sN', '--sorting-name', action='store_true', help="В указанной директории выполняет сортировку файлов по месяцам и годам исходя из имени файлов.")
    parser.add_argument('-rM', '--rename-meta', action='store_true', help="В указанной директории выполняет переименование файлы в формат 2013-01-01_21-21-09.JPEG, исходя из метаданных.")
    parser.add_argument('-rN', '--rename-name', action='store_true', help="В указанной директории выполняет переименование файлы в формат 2013-01-01_21-21-09.JPEG, исходя из имени файлов.")
    parser.add_argument('-iM', '--inside-meta', action='store_true', help="Добавляет метаданные в фото и видео, берёт из имени файла.")
    parser.add_argument('-iML', '--inside-meta-lite', action='store_true', help="Добавляет метаданные в фото и видео только на уровне файловой системы, влияет только на дату изминения. Эту функцию очень жалательно применять ко всем медиа файлам, которые имеют метаданные")
    # По умолчанию перевёл обработку на CUDA видеокарты, но функцию не удалял.
    #parser.add_argument('-iMC', '--inside-meta-cuda', action='store_true', help="Добавляет метаданные в фото и видео, берёт из имени файла, задействуется видеокарта.")
    parser.add_argument('-dF', '--delete-folder', action='store_true', help="В указанной директории удаляет все пустые папки и подпапки.")
    parser.add_argument('-mU', '--move-up', action='store_true', help="В указанной директории перемещает все файлы из подпапок в корневую.")
    parser.add_argument('-mUD', '--move-up-delete', action='store_true',help="В указанной директории перемещает все файлы из подпапок в корневую, затем удаляет пустые директории.")
    parser.add_argument('-fA', '--find-alien', action='store_true',help="В указанной директории поиск файлов, которые не числятся в списке и перемещение их в папку Strangers корневой папки.")




    # Парсим
    args = parser.parse_args()
    # Содержит директорию источник
    source_dir = args.directory

    # Проверяем, что директория - директория
    if not os.path.isdir(source_dir):
        print(f"Ошибка: '{source_dir}' не существует или это не директория, укажите директорию.")
        sys.exit(1)
    else:
        # Проверяем флаги
        if args.info:
            get_info_all_files(source_dir)

        if args.report:
            report(source_dir)

        # Обработка сортировки
        if args.sorting_meta and args.sorting_name:
            print("Ошибка: нельзя использовать одновременно сортировку по метаданным и по имени.")
            sys.exit(1)
        elif args.sorting_meta:
            print("Выполняется сортировка файлов по метаданным.")
            sorting_for_meta(source_dir)
        elif args.sorting_name:
            print("Выполняется сортировка файлов по имени.")
            sorting_for_name(source_dir)

        # Обработка переименования
        if args.rename_meta and args.rename_name:
            print("Ошибка: нельзя использовать одновременно переименование по метаданным и по имени.")
            sys.exit(1)
        elif args.rename_meta:
            print("Выполняется переименование файлов по метаданным.")
            rename_for_meta(source_dir)
        elif args.rename_name:
            print("Выполняется сортировка файлов по имени.")
            rename_for_name(source_dir)

        if args.inside_meta:
            # По умолчанию перевёл на куда ядра, функцию старую оставил
            print("Выполняется добавление метаданных в фото и видео.")
            insideMeta(source_dir)

        if args.inside_meta_lite:
            # По умолчанию перевёл на куда ядра, функцию старую оставил
            print("Выполняется изминение \"даты изминения\" в метаданных фото и видео.")
            insideMeta_lite(source_dir)

        if args.delete_folder:
            print("Выполняется удаление пустых директорий.")
            clearFolderDIr(source_dir)

        if args.move_up:
            print("Выполняется перемещение всех файлов в корневую директорию.")
            move_files_to_main_dir(source_dir)

        if args.move_up_delete:
            print("Выполняется перемещение всех файлов в корневую директорию, затем пустые папки будут удалены")
            move_files_to_main_dir(source_dir)
            clearFolderDIr(source_dir)

        if args.find_alien:
            print("Выполняется поиск чужеродных файлов")
            findAlienFiles(source_dir)



