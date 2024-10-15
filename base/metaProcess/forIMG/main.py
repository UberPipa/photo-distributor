import piexif
from datetime import datetime


def meta_process_PILLOW(basic_data) -> bool | str:
    """
    Ищем метаданные
    :param basic_data:
    :return:
    """

    location_file = basic_data['location_file']

    try:
        exif_data = piexif.load(location_file)
        # Выведите метаданные на экран
        if 'Exif' in exif_data:

            if piexif.ExifIFD.DateTimeOriginal in exif_data['Exif']:
                meta = exif_data['Exif'][piexif.ExifIFD.DateTimeOriginal]
                meta = meta.decode('utf-8')
                # Преобразуйте строку времени в объект datetime
                meta = datetime.strptime(meta, '%Y:%m:%d %H:%M:%S')
                # Форматируйте объект datetime в нужный формат
                meta = meta.strftime('%Y-%m-%d_%H-%M-%S')
                return meta
            else:
                if piexif.ExifIFD.DateTimeDigitized in exif_data['Exif']:
                    meta = exif_data['Exif'][piexif.ExifIFD.DateTimeDigitized]
                    meta = meta.decode('utf-8')
                    # Преобразуйте строку времени в объект datetime
                    meta = datetime.strptime(meta, '%Y:%m:%d %H:%M:%S')
                    # Форматируйте объект datetime в нужный формат
                    meta = meta.strftime('%Y-%m-%d_%H-%M-%S')
                    return meta
                else:
                    return False
    except:
        return False
