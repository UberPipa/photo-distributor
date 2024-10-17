import os

from base.basicProcess.basicCheck import check_type_file
from base.basicProcess.basicData import get_full_basic_data
from base.metaProcess.main import getEasyMeta
from base.parsNameProcess.main import get_data_from_name


def report(source_dir) -> None:
    """
    Предоставляет отчёт о вызванной директории
    :param source_dir:
    :return:
    """
    count_all_file = 0

    count_video = 0
    count_video_whithout_meta_date = 0
    count_video_whithout_name_date = 0
    count_video_whithout_two_signs = 0

    count_photo = 0
    count_photo_whithout_meta_date = 0
    count_photo_whithout_name_date = 0
    count_photo_whithout_two_signs = 0

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
                date = get_data_from_name(basic_data)

                count_all_file += 1

                if type_file == 'VID':
                    count_video += 1
                    if not meta:
                        count_video_whithout_meta_date += 1
                    if not date:
                        count_video_whithout_name_date += 1
                    if not meta and not date:
                        count_video_whithout_two_signs += 1
                        print(f"Не удалось вообще определить дату: {location_file}.")

                elif type_file == 'IMG':
                    count_photo += 1
                    if not meta:
                        count_photo_whithout_meta_date += 1
                    if not date:
                        count_photo_whithout_name_date += 1
                    if not meta and not date:
                        count_photo_whithout_two_signs += 1
                        print(f"Не удалось вообще определить дату: {location_file}.")

                else:
                    print("Попался не опознанный файл, вернуться позже")



    print(f"\nВсего файлов в директории \"{source_dir}\": {count_all_file}.")
    print(f"Сводка по видео:")
    print(f"    - Всего видео файлов: {count_video}.")
    print(f"    - Всего видео файлов без даты в мета данных: {count_video_whithout_meta_date}.")
    print(f"    - Всего видео файлов без даты в имени файла : {count_video_whithout_name_date}.")
    print(f"    - Всего видео файлов, где вообще не удалось определить дату: {count_video_whithout_two_signs}.")
    print(f"Сводка по фото:")
    print(f"    - Всего фото: {count_photo}.")
    print(f"    - Всего фото файлов без даты в мета данных: {count_photo_whithout_meta_date}.")
    print(f"    - Всего фото файлов без даты в имени файла : {count_photo_whithout_name_date}.")
    print(f"    - Всего фото файлов, где вообще не удалось определить дату: {count_photo_whithout_two_signs}.")