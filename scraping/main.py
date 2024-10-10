import os
import key_rate
import press_releases
import preprocessing

if not os.path.exists('../data/'):
    os.mkdir('../data')

print('Получение пресс-релизов...')
press_releases.get_press_releases()
print('Готово.')

print('Получение ключевых ставок...')
key_rate.get_key_rate()
print('Готово.')

print('Препроцессинг данных...')
preprocessing.make_preprocessing()
print('Готово.')
