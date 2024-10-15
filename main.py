import os
import sys

import conf
from base.example.example import get_info_all_files
import argparse


def run() -> None:
    """
    Запускает программу, тт нужно указывать этапы.
    :return:
    """
    parser = argparse.ArgumentParser(description="Консольная утилита для обработки фото и видео файлов")
    # Позиционные аргументы
    #parser.add_argument('input_dir', help="Директория для обработки на вход")

    # Параметры
    parser.add_argument('-d', '--directory', type=str, help="Директория для обработки на вход")
    parser.add_argument('-i', '--info', action='store_true', help="В указанной директории пробегает по каждому файлу и выводит по нему информацию.")
    parser.add_argument('-sM', '--sorting-meta', action='store_true', help="В указанной директории выполняет сортировку файлов по месяцам и годам исходя из метаданных.")
    #parser.add_argument('-sN', '--sorting-name', action='store_true', help="В указанной директории выполняет сортировку файлов по месяцам и годам исходя из имени файлов.")




    # Парсим
    args = parser.parse_args()

    # Содержит директорию источник
    source_dir = args.directory

    # Проверяем, что директория - директория
    if not os.path.isdir(source_dir):
        print(f"Ошибка: '{source_dir}' не существует или это не директория, укажите директорию.")
        sys.exit(1)


    # Проверяем флаг -i
    if args.info:
        get_info_all_files(source_dir)


