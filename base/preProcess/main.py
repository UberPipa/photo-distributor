import os

import ffmpeg
from PIL import Image


from base.basicProcess.basicCheck import check_type_file
from base.basicProcess.basicData import get_full_basic_data


def convertor(basic_data) -> str:
    """
    Берёт файл:
    - Сравнивает его с допустимыми расширениями, а именно "jpg" и "mp4"
    - Если всё ок, то не трогает
    - Если не совпадает регистр, то переименовывает файл
    - Если не совпадает расширение, то конвертирует в нужный формат

    В целом подготавливает файлы для дальнейшей работы, приводит к единому виду.
    """

    full_name = basic_data['full_name']
    name = basic_data['name']
    extension = basic_data['extension']
    type_file = basic_data['type_file']
    location_file = basic_data['location_file']
    location = os.path.dirname(location_file)

    if type_file == 'IMG':
        if extension != '.jpg':
            # Тут просто переименовываем
            if (
                    extension == ".jpeg" or
                    extension == ".JPEG" or
                    extension == ".JPG"
            ):

                old_name = location_file
                new_name = os.path.join(location, f"{name}.jpg")
                os.replace(old_name, new_name)

                new_name = f"{name}.jpg"
                return new_name

            else:
                dest = os.path.join(location, f"{name}.jpg")
                image = Image.open(location_file)
                mode = image.mode
                if mode != "RGB":
                    image = image.convert("RGB")

                image.save(dest, format="JPEG", quality=100, compression="lossless", iptc=True)
                image.close()
                # Удаляем старый файл
                os.remove(location_file)

                new_name = f"{name}.jpg"
                return new_name

        else:
            return full_name


    elif type_file == 'VID':
        if extension != '.mp4':
            # Тут просто переименовываем
            if extension == ".MP4":
                old_name = location_file
                new_name = os.path.join(location, f"{name}.mp4")
                os.replace(old_name, new_name)

                new_name = f"{name}.mp4"
                return new_name

            elif (
                    extension == ".MOV" or extension == ".mov" or
                    extension == ".3GP" or extension == ".3gp" or
                    extension == ".MPG" or extension == ".mpg" or
                    extension == ".AVI" or extension == ".avi" or
                    extension == ".FLV" or extension == ".flv" or
                    extension == ".MPEG" or extension == ".mpeg" or
                    extension == ".MKV" or extension == ".mkv"
            ):
                #  Тут уже конвертируем на полном серьёзе)
                dest = os.path.join(location, f"{name}.mp4")
                ffmpeg.input(location_file).output(dest, vcodec='libx264', preset='slow', crf=18, acodec='aac', audio_bitrate='192k', map_metadata=0).run()
                # Удаляем старый файл
                os.remove(location_file)

                new_name = f"{name}.mp4"
                return new_name

    else:
        return full_name