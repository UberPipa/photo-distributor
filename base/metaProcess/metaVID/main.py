import ffmpeg
from datetime import datetime, timedelta


def meta_process_FFMPEG(basic_data) -> bool | str:
    """

        Функция пытается получить метаданные с помощью FFMPEG

    """

    # Искомы тег

    try:
        location_file = basic_data['location_file']
        probe = ffmpeg.probe(location_file)
        meta = probe['format']['tags']['creation_time']

        dt = datetime.strptime(meta, "%Y-%m-%dT%H:%M:%S.%fZ")
        moscow_time = dt + timedelta(hours=3)
        meta = moscow_time.strftime("%Y-%m-%d_%H-%M-%S")

        return meta
    except:
        return False
