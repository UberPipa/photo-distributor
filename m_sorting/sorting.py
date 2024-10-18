import os
import shutil

from base.basicProcess.basicCheck import check_type_file
from base.basicProcess.basicData import get_full_basic_data
from base.metaProcess.main import getEasyMeta
import time

from base.parsNameProcess.main import get_data_from_name


def sorting_for_meta(source_dir) -> None:
    """
    Сортирует файлы по месяцам и годам. если в них есть метаданные. Если нет, то пропускает,
    сохраняет структуру папок.
    :param source_dir:
    :return:
    """
    s = 0
    for location, dirs, files in os.walk(source_dir):
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

                    location_year = os.path.join(location, str(year))
                    fixed_length = 2
                    location_month_in_year = os.path.join(location_year, f"{str(month).zfill(fixed_length)}")

                    if not os.path.exists(location_year):
                        """ Проверяем, есть ли dir года для этого файла, если нет, то создаём """
                        os.makedirs(os.path.join(location_year))
                        time.sleep(0.01)

                    if not os.path.exists(location_month_in_year):
                        """ Проверяем, есть ли dir месяца для этого файла, если нет, то создаём """
                        os.makedirs(os.path.join(location_month_in_year))
                        time.sleep(0.01)

                    """ Двигаем файлы """
                    shutil.move(location_file, location_month_in_year)
                    time.sleep(0.01)

    print(f"Всего отсортировано файлов по метаданным: {s}.")


def sorting_for_name(source_dir) -> None:
    """
    Сортирует файлы по месяцам и годам. если удалось спарсить дату из имени. Если нет, то пропускает,
    сохраняет структуру папок.
    :param source_dir:
    :return:
    """
    s = 0
    for location, dirs, files in os.walk(source_dir):
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

                    location_year = os.path.join(location, str(year))
                    fixed_length = 2
                    location_month_in_year = os.path.join(location_year, f"{str(month).zfill(fixed_length)}")

                    if not os.path.exists(location_year):
                        """ Проверяем, есть ли dir года для этого файла, если нет, то создаём """
                        os.makedirs(os.path.join(location_year))
                        time.sleep(0.01)

                    if not os.path.exists(location_month_in_year):
                        """ Проверяем, есть ли dir месяца для этого файла, если нет, то создаём """
                        os.makedirs(os.path.join(location_month_in_year))
                        time.sleep(0.01)

                    """ Двигаем файлы """
                    shutil.move(location_file, location_month_in_year)
                    time.sleep(0.01)

    print(f"Всего отсортировано файлов по метаданным: {s}.")