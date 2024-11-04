import os
import shutil

import ffmpeg
import piexif


from PIL import Image
from datetime import datetime
from base.basicProcess.basicCheck import check_type_file
from base.basicProcess.basicData import get_full_basic_data
from base.parsNameProcess.main import get_data_from_name


def insideMetaVID_no_CUDA(basic_data):
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

    if date:
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
            metadata=f'creation_time={new_datetime}',  # Устанавливаем дату съёмки как creation_time
            y='-y'
        )

        # Запускаем ffmpeg
        ffmpeg.run(stream, overwrite_output=True)

        # Удаляем старое видео
        os.remove(location_file)

        # Переименовываем временный файл в оригинальное имя
        os.rename(temp_file, location_file)

        # Устанавливаем даты создания и изменения файла на уровне файловой системы
        new_timestamp = date_object.timestamp()
        os.utime(location_file, (new_timestamp, new_timestamp))  # Устанавливаем atime и mtime


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

    if date:
        # Подготавливаем дату
        date_object = datetime.strptime(date, "%Y-%m-%d_%H-%M-%S")
        new_datetime = date_object.strftime("%Y-%m-%dT%H:%M:%S")

        # Создаем временное имя файла для нового видео
        temp_file = os.path.join(os.path.dirname(location_file), f"{name}_temp.{extension}")

        # Копируем видео с новыми метаданными и аппаратным ускорением GPU
        stream = ffmpeg.input(location_file)
        stream = ffmpeg.output(
            stream,
            stream,
            temp_file,
            vcodec='h264_nvenc',  # Используем NVENC для аппаратного кодирования на GPU
            preset='fast',         # Оптимизировано для скорости
            cq=26,                 # Высокое качество с компромиссами для скорости
            acodec='copy',         # Копируем оригинальный аудиопоток без перекодирования
            metadata=f'creation_time={new_datetime}',  # Устанавливаем дату съёмки как creation_time
            y='-y'

            # stream,
            # temp_file,  # Сохраняем во временный файл
            # vcodec = 'h264_nvenc',  # Кодирование на GPU
            # preset = 'p5',  # Высокое качество
            # qp = 18,  # Качество
            # b_v = '10M',  # Установленный битрейт для сохранения качества
            # acodec = 'aac',
            # audio_bitrate = '192k',
            # metadata = f'creation_time={new_datetime}',  # Устанавливаем дату съёмки как creation_time
            # y = '-y'
        )

        # Запускаем ffmpeg
        ffmpeg.run(stream, overwrite_output=True)

        # Удаляем старое видео
        os.remove(location_file)

        # Переименовываем временный файл в оригинальное имя
        os.rename(temp_file, location_file)

        # Устанавливаем даты создания и изменения файла на уровне файловой системы
        new_timestamp = date_object.timestamp()
        os.utime(location_file, (new_timestamp, new_timestamp))  # Устанавливаем atime и mtime


def insideMetaIMG(basic_data):
    """
    Интерирует метаданные из имени в файл.
    """
    full_name = basic_data['full_name']
    name = basic_data['name']
    extension = basic_data['extension']
    type_file = basic_data['type_file']
    location_file = basic_data['location_file']

    date = get_data_from_name(basic_data)

    if date:
        # Удаляем все метаданные из файла
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

        # Устанавливаем дату съёмки, создания и изменения
        exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = new_datetime  # Дата съёмки
        exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = new_datetime  # Дата оцифровки
        exif_dict["0th"][piexif.ImageIFD.DateTime] = new_datetime  # Дата создания и изменения

        # Преобразуем метаданные в бинарную строку
        exif_bytes = piexif.dump(exif_dict)

        # Сохраняем изображение с метаданными во временный файл
        image.save(temp_file, "jpeg", exif=exif_bytes)

        # Удаляем старый файл
        os.remove(location_file)

        # Переименовываем временный файл в оригинальное имя
        os.rename(temp_file, location_file)

        # Устанавливаем даты создания и изменения файла
        new_timestamp = date_object.timestamp()
        os.utime(location_file, (new_timestamp, new_timestamp))  # Установка mtime и atime


def insideMeta_lite(source_dir):
    """
    Меняет дату изминения в соответвкии с датой из метаданных. Способ универсальный, поэтому подходит для всех.
    По идее функция должна быть обязательная.
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
                    # Подготавливаем дату
                    date_object = datetime.strptime(date, "%Y-%m-%d_%H-%M-%S")

                    # Устанавливаем даты создания и изменения файла
                    new_timestamp = date_object.timestamp()
                    os.utime(location_file, (new_timestamp, new_timestamp))  # Установка mtime и atime

        print(f"Всего переписал \"Время изминения\": {s}.")


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
