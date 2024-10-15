import os

from base.basicProcess.basicCheck import check_type_file
from base.basicProcess.basicData import get_full_basic_data
from base.metaProcess.main import getEasyMeta
from base.parsNameProcess.main import get_data_from_name
from conf import srcDir


def get_info_all_files() -> None:
    """
    Шаблон в цикле, в него можно пихать разные функции
    :return:
    """
    s = 0
    for location, dirs, files in os.walk(srcDir):

        for file in os.listdir(location):
            if check_type_file(file):
                basic_data = get_full_basic_data(file, location)
                full_name = basic_data['full_name']
                name = basic_data['name']
                extension = basic_data['extension']
                type_file = basic_data['type_file']
                location_file = basic_data['location_file']

                #convertor(basic_data)


                meta = getEasyMeta(basic_data)
                date = get_data_from_name(basic_data)

                s += 1
                print(f"Файл {s}: {full_name};")
                print(f"Метаданные: {meta};" )
                print(f"Парс по имени: {date}.\n")