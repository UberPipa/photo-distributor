from base.example.example import get_info_all_files
import argparse


def run() -> None:
    """
    Запускает программу, тт нужно указывать этапы.
    :return:
    """
    parser = argparse.ArgumentParser(description="Консольная утилита для обработки фото и видео файлов")
    # Позиционные аргументы
    parser.add_argument('input_dir', help="Директория для обработки на вход")

    # Параметры
    parser.add_argument('-i', '--info', action='store_true', help="")


    # Парсим
    args = parser.parse_args()


    # Проверяем флаг -i для вывода Hello, World!
    if args.info:
        get_info_all_files()


