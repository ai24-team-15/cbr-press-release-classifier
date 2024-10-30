import os
import key_rate
import press_releases
import cur_usd
import inflation
import preprocessing
from logger import logger
import sys
from s3client import save_data_to_s3
from config import Config

sys.path.insert(1, os.path.join(sys.path[0], '..'))

def main():
    if not os.path.exists('../data/'):
        os.mkdir('../data')

    logger.info('Получение пресс-релизов.')
    press_releases.get_press_releases()
    logger.info('Получение пресс-релизов завершено.')

    logger.info('Получение ключевых ставок.')
    key_rate.get_key_rate()
    logger.info('Получение ключевых ставок завершено.')

    logger.info('Получение курса доллара.')
    cur_usd.get_cur_usd()
    logger.info('Получение курса доллара завершено.')

    logger.info('Получение данных по инфляции.')
    inflation.get_inflation()
    logger.info('Получение данных по инфляции завершено.')

    logger.info('Подготовка данных.')
    preprocessing.make_preprocessing()
    logger.info('Подготовка данных завершена.')

    logger.info('Загрузка данных в S3.')
    save_data_to_s3(
        access_key=Config.access_key,
        secret_key=Config.secret_key
    )
    logger.info('Загрузка данных в S3 завершена.')


if __name__ == '__main__':
    main()
