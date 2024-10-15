from base.metaProcess.forIMG.main import meta_process_PILLOW
from base.metaProcess.metaVID.main import meta_process_FFMPEG
from conf import type_file_IMG, type_file_VID


def meta_unification(basic_data) -> None | str:
    """
    Функция сливает вместе метаданные от фото и видео файлов, сделано для удобства обработки.
    Тут можно выбирать что именно будет получать от мета и какой глубины
    :param basic_data:
    :return:
    """

    # Достаём тип файла
    type_file = basic_data['type_file']

    # Если фото, то:
    if type_file == type_file_IMG:
        meta = meta_process_PILLOW(basic_data)
        return meta
        pass

    # Если видео, то:
    elif type_file == type_file_VID:
        meta = meta_process_FFMPEG(basic_data)
        return meta
        pass

    else:
        return False