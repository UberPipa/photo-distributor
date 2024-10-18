import os
import sys

import conf
from base.example.example import get_info_all_files
import argparse

from m_rename.rename import rename_for_meta, rename_for_name
from m_report.report import report
from m_sorting.sorting import sorting_for_meta, sorting_for_name


def run() -> None:
    """
    Запускает программу, тт нужно указывать этапы.
    :return:
    """
    parser = argparse.ArgumentParser(description="Консольная утилита для обработки фото и видео файлов")
    # Позиционные аргументы
    #parser.add_argument('input_dir', help="Директория для обработки на вход")

    # Параметры
    parser.add_argument('-d', '--directory', type=str, required=True,  help="Директория для обработки на вход")
    parser.add_argument('-i', '--info', action='store_true', help="В указанной директории пробегает по каждому файлу и выводит по нему информацию.")
    parser.add_argument('-r', '--report', action='store_true', help="По указанной директории выводит побробную информацию по всем файлам.")
    parser.add_argument('-sM', '--sorting-meta', action='store_true', help="В указанной директории выполняет сортировку файлов по месяцам и годам исходя из метаданных.")
    parser.add_argument('-sN', '--sorting-name', action='store_true', help="В указанной директории выполняет сортировку файлов по месяцам и годам исходя из имени файлов.")
    parser.add_argument('-rM', '--rename-meta', action='store_true',help="В указанной директории выполняет переименование файлы в формат 2013-01-01_21-21-09.JPEG, исходя из метаданных.")
    parser.add_argument('-rN', '--rename-name', action='store_true',help="В указанной директории выполняет переименование файлы в формат 2013-01-01_21-21-09.JPEG, исходя из имени файлов.")


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


