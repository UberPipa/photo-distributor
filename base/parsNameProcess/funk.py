import datetime
import re
from typing import Union


def chek_date(date, mask) -> bool:
    """
    Быстрый костыль, проверяет что бы год не был меньше 2000 года.
    """
    try:
        date_obj = datetime.datetime.strptime(date, mask)
        if date_obj.year > 2000:
            return True
        else:
            return False
    except ValueError:
        return False


def get_str_from_name(basic_data) -> Union[bool, str]:
    """
    Функция c регулярками для обнаружения дат из имён файлов
    Возвращает или дату или False
    После этой функции дату ещё нужно обработать.
    :param basic_data:
    :return:
    """

    def chek_date(date, mask) -> bool:
        try:
            date_obj = datetime.datetime.strptime(date, mask)
            if date_obj.year > 2000:
                return True
            else:
                return False
        except ValueError:
            return False

    name = basic_data['name']

    pattern_1 = re.findall(r'(^\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2})', name)
    pattern_2 = re.findall(r'^(\d{8}_\d{6})', name)
    pattern_3 = re.findall(r'(^\d{2}-\d{2}-\d{2}_\d{4})', name)
    pattern_3_1 = re.findall(r'(^\d{2}_\d{2}_\d{2})', name)
    pattern_4 = re.search(r'^((VID|IMG|WP)_\d{8}_\d{6})', name)
    pattern_4_1 = re.search(r'^((VID|IMG)-\d{8}-)', name)
    pattern_5 = re.search(r'^(?=.{12}$)\d{12}$', name)
    pattern_5_1 = re.search(r'^(?=.{8,11}$)\d{8,11}$', name)
    pattern_6 = re.findall(r'\b\d{11}-\d{3}\b', name)  # Всего одно фото
    pattern_7 = re.search(r'\b\d{13}\b', name)
    pattern_8 = re.search(r'\b\d{1,2}_\d{1,2}_\d{4}\b', name)
    pattern_9 = re.search(r'\bScreenshot_\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}-\d+\b', name)
    pattern_10 = re.findall(r'photo\d{8}', name)


    if pattern_1:
        """ Ищет в форматах 2016-08-10 17-51-02 """
        pattern_1 = ' '.join(pattern_1)
        mask = '%Y-%m-%d %H-%M-%S'
        if chek_date(pattern_1, mask):
            """ Пробуем преобразовать в дату и время по маске """
            date = pattern_1
        else:
            date = False
        pass
        return date

    elif pattern_2:
        """ Ищет в форматах 20221231_231809 """
        pattern_2 = ' '.join(pattern_2)
        mask = '%Y%m%d_%H%M%S'
        if chek_date(pattern_2, mask):
            """ Пробуем преобразовать в дату и время по маске """
            date = pattern_2
        else:
            date = False
        pass
        return date

    elif pattern_3:
        """ Ищет в форматах 05-05-09_1841 """
        pattern_3 = ' '.join(pattern_3)
        mask = '%d-%m-%y_%H%M'
        if chek_date(pattern_3, mask):
            """ Пробуем преобразовать в дату и время по маске """
            date = pattern_3
        else:
            date = False
        pass
        return date

    elif pattern_3_1:
        """ Ищет в форматах 07_12_14 """
        pattern_3_1 = ' '.join(pattern_3_1)
        mask = '%d_%m_%y'
        if chek_date(pattern_3_1, mask):
            """ Пробуем преобразовать в дату и время по маске """
            date = pattern_3_1
        else:
            date = False
        pass
        return date

    elif pattern_4:
        """ Ищет в форматах IMG_20150806_102921 """
        pattern_4 = re.findall(r'\d{8}_\d{6}', name)
        pattern_4 = ' '.join(pattern_4)
        mask = '%Y%m%d_%H%M%S'
        if chek_date(pattern_4, mask):
            """ Пробуем преобразовать в дату и время по маске """
            date = pattern_4
        else:
            date = False
        pass
        return date

    elif pattern_4_1:
        """ Ищет в форматах VID-20190525-WA0018 """
        pattern_4_1 = re.findall(r'\d{8}', name)
        pattern_4_1 = ' '.join(pattern_4_1)
        mask = '%Y%m%d'
        if chek_date(pattern_4_1, mask):
            """ Пробуем преобразовать в дату и время по маске """
            date = pattern_4_1
        else:
            date = False
        pass
        return date

    elif pattern_5:
        """ 
        Ищет в строках, где только 12 цифр подряд - 291020131402.
        Eсли не находит, то вернёт False
        """
        mask_1 = '%d%m%Y%H%M'
        mask_2 = '%d%m%Y'
        if chek_date(name, mask_1):
            """ Пробуем преобразовать в дату и время по маске """
            date = name
        else:
            if chek_date(name[:8], mask_2):
                """ Пробуем преобразовать только дату по маске """
                date = name[:8]
            else:
                """ Если дата не действительна, то False """
                date = False
        pass
        return date

    elif pattern_5_1:
        """ Ищет в строках, где от 8 до 11 цифр подряд - 29102013140 """
        mask = '%d%m%Y'
        if chek_date(name[:8], mask):
            """ Пробуем преобразовать в дату по маске """
            date = name[:8]
        else:
            date = False
        pass
        return date

    elif pattern_6:
        """ Ищет в строках 03062012832-001 """
        mask = '%d%m%Y'
        if chek_date(name[:8], mask):
            """ Пробуем преобразовать в дату по маске """
            date = name[:8]
        else:
            date = False
        pass
        return date

    elif pattern_7:
        """ Ищет в строках 2014628195824 """

        mask = '%Y%m%d'

        if chek_date(name[:7], mask):
            """ Пробуем преобразовать в дату по маске """
            date = name[:7]
        else:
            date = False
        pass
        return date

    elif pattern_8:
        """ Ищет в строках 2_08_2013 (102) """
        mask = '%d_%m_%Y'
        if chek_date(name[:9], mask):
            """ Пробуем преобразовать в дату по маске """
            date = name[:9]
        else:
            date = False
        pass
        return date

    elif pattern_9:
        """ Ищет в строках Screenshot_2016-06-08-15-25-28-1 """
        mask = '%Y-%m-%d-%H-%M-%S'
        pattern_9 = re.findall(r'\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}', name)
        pattern_9 = ' '.join(pattern_9)
        if chek_date(pattern_9, mask):
            """ Пробуем преобразовать в дату по маске """
            date = pattern_9
        else:
            date = False
        pass
        return date

    elif pattern_10:
        """ Ищет в строках photo20131110 """
        mask = '%Y%m%d'
        pattern_10 = ' '.join(pattern_10)
        if chek_date(pattern_10[5:], mask):
            """ Пробуем преобразовать в дату по маске """
            date = pattern_10[5:]
            # Исправление с багом: 16988_____ 1110-13-20_00-00-00.jpg_______ photo20131110-8779-1pxc8dn.jpg____________________ Найдено у 16872 файлов _______Не найдено у 116 файлов
            date = date[6:] + date[4:6] + date[:4]
        else:
            date = False
        pass
        return date

    else:
        pass
        return False


def get_correct_date(date) -> str:
    """
    Поучает строку с датой обрабатывает все возможные варианты, для приведения к единому виду.
    Если чего то не хватает, то дописывает нули.
    :param date:
    :return:
    """
    # name = basic_data['name']
    pattern_1 = re.search(r'\d{4}(:|_|-| )\d{2}(:|_|-| )\d{2}.*?\d{2}(:|_|-| )\d{2}(:|_|-| )\d{2}', date)
    pattern_2 = re.search(r'\d{2}(:|_|-| )\d{2}(:|_|-| )\d{2}.*?\d{4}', date)
    pattern_3 = re.search(r'\d{8}(:|_|-| )\d{6}', date)
    pattern_4 = re.search(r'\d{12}', date)
    pattern_5 = re.search(r'\d{8}', date)
    pattern_6 = re.search(r'(\d{2}_\d{2}_\d{2})', date)

    if pattern_1:
        """ 
        Ищет в форматах 2016?08?10?17?51?02.
        Собирает строку в 2021-06-24_11-13-11
        """

        year = date[:4]
        month = date[5:7]
        day = date[8:10]
        hour = date[11:13]
        minutes = date[14:16]
        sec = date[17:19]

        date = f'{year}-{month}-{day}_{hour}-{minutes}-{sec}'

        pass
        return date


    elif pattern_2:
        """ 
        Ищет в форматах 23-07-09_1614.
        """

        year = date[6:8]
        month = date[3:5]
        day = date[:2]
        hour = date[9:11]
        minutes = date[11:13]

        date = f'20{year}-{month}-{day}_{hour}-{minutes}-00'

        pass
        return date

    elif pattern_3:
        """ 
        Ищет в форматах 20160322_172205.
        """

        year = date[:4]
        month = date[4:6]
        day = date[6:8]
        hour = date[9:11]
        minutes = date[11:13]
        sec = date[13:15]

        date = f'{year}-{month}-{day}_{hour}-{minutes}-{sec}'

        pass
        return date


    elif pattern_4:
        """ 
        Ищет в форматах 301220121101.
        """

        year = date[4:8]
        month = date[2:4]
        day = date[:2]
        hour = date[8:10]
        minutes = date[10:12]

        date = f'{year}-{month}-{day}_{hour}-{minutes}-00'

        pass
        return date


    elif pattern_5:
        """
        Ищет в форматах 22122012.
        """
        year = date[4:8]
        month = date[2:4]
        day = date[:2]

        # Исправление бага с не правильной датой - 0729-19-20_00-00-00 (20190729)
        if int(year) > 2000:
            # Стандартный сценарий
            date = f'{year}-{month}-{day}_00-00-00'
        else:
            # Переопределяем дату
            year = date[:4]
            month = date[4:6]
            day = date[6:8]
            date = f'{year}-{month}-{day}_00-00-00'

        pass
        return date


    elif pattern_6:
        """
        Ищет в форматах 07_12_14
        """
        year = date[6:8]
        month = date[3:5]
        day = date[:2]


        date = f'20{year}-{month}-{day}_00-00-00'

        pass
        return date


    else:
        pass
        #print('Не смог преобразовать дату')
        #print(date)
        #breakpoint()
        # return date