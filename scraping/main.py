import os
import key_rate
import press_releases
import preprocessing
from logger import logger


def main():
    if not os.path.exists('../data/'):
        os.mkdir('../data')

    logger.info('Получение пресс-релизов.')
    press_releases.get_press_releases()
    logger.info('Получение пресс-релизов завершено.')

    logger.info('Получение ключевых ставок.')
    key_rate.get_key_rate()
    logger.info('Получение ключевых ставок завершено.')

    logger.info('Подготовка данных.')
    preprocessing.make_preprocessing()
    logger.info('Подготовка данных завершена.')


if __name__ == '__main__':
    main()
