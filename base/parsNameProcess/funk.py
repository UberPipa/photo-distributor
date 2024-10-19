import datetime
import re
from typing import Union


def chek_date(date: str, mask: str) -> bool:
    """
    Проверяет корректность даты и года (не меньше 2000 года).
    """
    try:
        date_obj = datetime.datetime.strptime(date, mask)
        return date_obj.year > 2000
    except ValueError:
        return False


def get_str_from_name(basic_data: dict) -> Union[bool, str]:
    """
    Функция для обнаружения дат из имён файлов с помощью регулярных выражений.
    Возвращает дату, если она найдена, или False.
    """

    name = basic_data['name']

    # Словарь с регулярными выражениями и масками для обработки дат
    patterns = [
        (r'(^\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2})', '%Y-%m-%d %H-%M-%S'),
        (r'^(\d{8}_\d{6})', '%Y%m%d_%H%M%S'),
        (r'(^\d{2}-\d{2}-\d{2}_\d{4})', '%d-%m-%y_%H%M'),
        (r'(^\d{2}_\d{2}_\d{2})', '%d_%m_%y'),
        (r'^((VID|IMG)_\d{8}_\d{6})', '%Y%m%d_%H%M%S'),
        (r'^((VID|IMG)-\d{8}-)', '%Y%m%d'),
        (r'^(?=.{12}$)\d{12}$', '%d%m%Y%H%M'),
        (r'^(?=.{8,11}$)\d{8,11}$', '%d%m%Y'),
        (r'\b\d{11}-\d{3}\b', '%d%m%Y'),
        (r'\b\d{13}\b', '%Y%m%d'),
        (r'\b\d{1,2}_\d{1,2}_\d{4}\b', '%d_%m_%Y'),
        (r'Screenshot_\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}', '%Y-%m-%d-%H-%M-%S'),
        (r'photo\d{8}', '%Y%m%d'),
        (r'^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}', '%Y-%m-%d_%H-%M-%S')
    ]

    # Проверка по каждому паттерну
    for pattern, mask in patterns:
        match = re.findall(pattern, name)
        if match:
            match_str = ' '.join(match)
            if chek_date(match_str, mask):
                return match_str

    return False


def get_correct_date(date: str) -> str:
    """
    Обрабатывает строку с датой и приводит её к единому формату.
    """
    patterns = [
        (r'\d{4}(:|_|-| )\d{2}(:|_|-| )\d{2}.*?\d{2}(:|_|-| )\d{2}(:|_|-| )\d{2}', '%Y-%m-%d_%H-%M-%S'),
        (r'\d{2}(:|_|-| )\d{2}(:|_|-| )\d{2}.*?\d{4}', '20%y-%m-%d_%H-%M-00'),
        (r'\d{8}(:|_|-| )\d{6}', '%Y-%m-%d_%H-%M-%S'),
        (r'\d{12}', '%Y-%m-%d_%H-%M-00'),
        (r'\d{8}', '%Y-%m-%d_00-00-00'),
        (r'(\d{2}_\d{2}_\d{2})', '20%y-%m-%d_00-00-00')
    ]

    for pattern, mask in patterns:
        match = re.search(pattern, date)
        if match:
            date_obj = datetime.datetime.strptime(match.group(), mask)
            return date_obj.strftime('%Y-%m-%d_%H-%M-%S')

    return 'Invalid date format'