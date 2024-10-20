import os
import shutil

import ffmpeg
import piexif


from PIL import Image
from datetime import datetime
from base.basicProcess.basicCheck import check_type_file
from base.basicProcess.basicData import get_full_basic_data
from base.parsNameProcess.main import get_data_from_name


def insideMetaVID(basic_data):
    """
    Интерирует метаданные из имени в файл,
    Копирует видео в ту же папку с новыми заголовками.
    Старое видео удаляется.
    """
    full_name = basic_data['full_name']
    name = basic_data['name']
    extension = basic_data['extension']
    type_file = basic_data['type_file']
    location_file = basic_data['location_file']

    date = get_data_from_name(basic_data)

    # Подготавливаем дату
    date_object = datetime.strptime(date, "%Y-%m-%d_%H-%M-%S")
    new_datetime = date_object.strftime("%Y-%m-%dT%H:%M:%S")

    # Создаем временное имя файла для нового видео
    temp_file = os.path.join(os.path.dirname(location_file), f"{name}_temp.{extension}")

    # Копируем видео с новыми метаданными
    stream = ffmpeg.input(location_file)
    stream = ffmpeg.output(
        stream,
        temp_file,  # Сохраняем во временный файл
        vcodec='libx264',
        preset='slow',
        crf=18,
        acodec='aac',
        audio_bitrate='192k',
        metadata=f'creation_time={new_datetime}',
        c='copy',
        y='-y'
    )

    # Запускаем ffmpeg
    ffmpeg.run(stream, overwrite_output=True)

    # Удаляем старое видео
    os.remove(location_file)

    # Переименовываем временный файл в оригинальное имя
    os.rename(temp_file, location_file)


def insideMetaIMG(basic_data):
    """
    Интерирует метаданные из имени в файл
    """
    full_name = basic_data['full_name']
    name = basic_data['name']
    extension = basic_data['extension']
    type_file = basic_data['type_file']
    location_file = basic_data['location_file']

    date = get_data_from_name(basic_data)
    #print(date)
    # Удаляем все мета данные из файла
    # Открываем изображение
    image = Image.open(location_file)
    image.getexif().clear()

    # Сохраняем изображение без метаданных во временный файл
    temp_file = os.path.join(os.path.dirname(location_file), f"{name}_temp.{extension}")
    image.save(temp_file)

    # Открываем заново сохраненное изображение
    image = Image.open(temp_file)
    exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "Interop": {}, "1st": {}, "thumbnail": None}

    # Подготавливаем дату
    date_object = datetime.strptime(date, "%Y-%m-%d_%H-%M-%S")
    new_datetime = date_object.strftime("%Y:%m:%d %H:%M:%S")

    exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = new_datetime
    exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = new_datetime

    # Преобразуем метаданные в бинарную строку
    exif_bytes = piexif.dump(exif_dict)

    # Сохраняем изображение с метаданными во временный файл
    image.save(temp_file, "jpeg", exif=exif_bytes)

    # Удаляем старый файл
    os.remove(location_file)

    # Переименовываем временный файл в оригинальное имя
    os.rename(temp_file, location_file)


def insideMeta(source_dir) -> None:
    """
    Добавляет метаданные в фото и видео, берёт из имени файла.
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


                if type_file == 'IMG':
                    # Интегрируем мета данные с переносом
                    insideMetaIMG(basic_data)

                if type_file == 'VID':
                    # Интегрируем мета данные с переносом
                    insideMetaVID(basic_data)

                s += 1

    print(f"Всего интегрированно метаданных: {s}.")
