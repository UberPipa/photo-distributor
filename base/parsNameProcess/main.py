import datetime
import re
from typing import Union

from base.parsNameProcess.funk import get_str_from_name, get_correct_date


def get_data_from_name(basic_data) -> Union[bool, str]:
    """
    Парсом имени файла получает дату, если что дополняет нулями,
    отдаёт строку или False.
    """
    raw_date = get_str_from_name(basic_data)

    if raw_date:
        date = raw_date[:19]
        date = get_correct_date(date)
        return date
    else:
        return False
