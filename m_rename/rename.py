import os


from base.basicProcess.basicCheck import check_type_file
from base.basicProcess.basicData import get_full_basic_data
from base.metaProcess.main import getEasyMeta
from base.parsNameProcess.main import get_data_from_name


def rename_for_meta(dir) -> None:
    """
    Переименовывает файлы в формат 2013-01-01_21-21-09.JPEG, исходя из метаданных.
    Если файл с таким именем уже существует, то добавляет суффикс +1, +2 и т.д.
    :param dir:
    :return:
    """

    s = 0
    for location, dirs, files in os.walk(dir):

        for file in os.listdir(location):
            if check_type_file(file):
                basic_data = get_full_basic_data(file, location)
                full_name = basic_data['full_name']
                name = basic_data['name']
                extension = basic_data['extension']
                type_file = basic_data['type_file']
                location_file = basic_data['location_file']

                meta = getEasyMeta(basic_data)

                if meta:
                    s += 1

                    year = meta[:4]
                    month = meta[5:7]
                    day = meta[8:10]
                    hour = meta[11:13]
                    minutes = meta[14:16]
                    second = meta[17:19]

                    # Формируем новое имя файла
                    new_name = f"{year}-{month}-{day}_{hour}-{minutes}-{second}{extension}"
                    dir_name = os.path.dirname(location_file)
                    new_location_file = os.path.join(dir_name, new_name)

                    # Проверяем, существует ли файл с таким именем, и добавляем суффиксы при необходимости
                    count = 1
                    while os.path.exists(new_location_file):
                        # Если файл существует, добавляем суффикс _1, _2 и т.д.
                        new_name = f"{year}-{month}-{day}_{hour}-{minutes}-{second}_{count}{extension}"
                        new_location_file = os.path.join(dir_name, new_name)
                        count += 1

                    # Переименовываем файл
                    os.rename(location_file, new_location_file)

    print(f"Всего переименовано файлов по метаданным: {s}.")


def rename_for_name(dir) -> None:
    """
    Переименовывает файлы в формат 2013-01-01_21-21-09.JPEG, исходя из имени файлов.
    Если файл с таким именем уже существует, то добавляет суффикс +1, +2 и т.д.
    :param source_dir:
    :return:
    """


    s = 0
    for location, dirs, files in os.walk(dir):

        for file in os.listdir(location):
            if check_type_file(file):
                basic_data = get_full_basic_data(file, location)
                full_name = basic_data['full_name']
                name = basic_data['name']
                extension = basic_data['extension']
                type_file = basic_data['type_file']
                location_file = basic_data['location_file']

                date = get_data_from_name(basic_data)

                if date:
                    s += 1

                    year = date[:4]
                    month = date[5:7]
                    day = date[8:10]
                    hour = date[11:13]
                    minutes = date[14:16]
                    second = date[17:19]

                    # Формируем новое имя файла
                    new_name = f"{year}-{month}-{day}_{hour}-{minutes}-{second}{extension}"
                    dir_name = os.path.dirname(location_file)
                    new_location_file = os.path.join(dir_name, new_name)

                    # Проверяем, существует ли файл с таким именем, и добавляем суффиксы при необходимости
                    count = 1
                    while os.path.exists(new_location_file):
                        # Если файл существует, добавляем суффикс _1, _2 и т.д.
                        new_name = f"{year}-{month}-{day}_{hour}-{minutes}-{second}_{count}{extension}"
                        new_location_file = os.path.join(dir_name, new_name)
                        count += 1

                    # Переименовываем файл
                    os.rename(location_file, new_location_file)

    print(f"Всего переименовано файлов по метаданным: {s}.")