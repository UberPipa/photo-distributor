from base.metaProcess.logic import meta_unification


def getEasyMeta(basic_data) -> None | str:
    """
    Так или иначе работает с метаданными. Проходная функция, что бы скрыть логику распределения на фото и видео.
    Возвращает метаданные одного вида, берут из тега, одного тега, где дата съёмки.
    :param basic_data:
    :return: "2015:10:01 16:45:07"
    """

    try:
        meta = meta_unification(basic_data)
        #print(meta)
        return meta
    except UserWarning:
        pass
    except AttributeError:
        return False