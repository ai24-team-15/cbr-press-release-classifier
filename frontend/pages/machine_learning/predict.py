import asyncio
import streamlit as st
import pandas as pd
from tools.api import client
from tools.config import log as logger


# Заголовок страницы
st.header('Прогнозирование решения ЦБ')

# Получение доступных моделей с сервера с использованием асинхронного запроса
models = asyncio.run(client.get_models('/get_models'))

# Составление списка ID моделей
model_ids = [model['model_id'] for model in models]

# Выбор модели для предсказания с помощью радио-кнопок
model_id = st.radio('Выберите модель', model_ids)

# Отображение информации о выбранной модели
st.subheader('Выбрана модель:')
for model in models:
    if model_id == model['model_id']:
        for key in model:
            # Если это гиперпараметры модели, отображаем их
            if key == 'hyperparameters':
                if len(model[key]) > 0:
                    st.markdown(f'`{key}`:')
                for k in model[key]:
                    st.markdown(f'* `{k}`: {model[key][k]}')
            # Иначе отображаем стандартные параметры модели
            else:
                st.markdown(f'`{key}`: {model[key]}')

# Выбор источника данных для предсказания
source = st.radio("Данные для предсказания",
                  ["Ввести текст пресс-релиза",
                   "Загрузить txt файл",
                   "Использовать последний пресс-релиз"])

# Инициализация переменной для текста пресс-релиза
release = None

# Загрузка последнего пресс-релиза из файла CSV
last_release = pd.read_csv('./data/cbr-press-releases.csv').tail(1)

# Обработка выбранного источника данных
if source == "Ввести текст пресс-релиза":
    release = st.text_input('Введите текст пресс-релиза')  # Текстовое поле для ввода

elif source == "Загрузить txt файл":
    # Загрузка текстового файла с пресс-релизом
    file = st.file_uploader('Загрузите txt файл с текстом пресс-релиза', type='txt')
    if file:
        release = file.read().decode("utf-8")  # Декодирование содержимого файла в строку

elif source == "Использовать последний пресс-релиз":
    release = last_release['release'].values[0]  # Используем последний пресс-релиз из файла CSV

# Если текст пресс-релиза был введен или загружен, показываем его на экране
if release:
    last_release['release'] = release
    st.subheader('Текущий текст пресс-релиза')
    st.text_area('', release, height=200)  # Отображение текста пресс-релиза в текстовой области

# Кнопка для получения предсказания модели
if st.button('Получить предсказание'):
    try:
        # Асинхронный запрос на предсказание с выбранной моделью
        prediction = asyncio.run(client.predict('/predict', model_id=model_id))
    except Exception as e:
        logger.error("Ошибка при получении предсказания моделью %s: %s", model_id, e)
        raise e

    logger.info("Предсказание модели %s успешно получено.", model_id)

    # Отображение предсказания модели
    st.subheader('Предсказание модели')
    if prediction['predict'] == -1:
        st.write('На следующем заседании ставка будет снижена.')
    elif prediction['predict'] == 0:
        st.write('На следующем заседании ставка будет сохранена.')
    else:
        st.write('На следующем заседании ставка будет повышена.')
