import asyncio
import pandas as pd
import streamlit as st
from tools.config import log as logger
from tools.api import client


# Установка заголовка приложения
st.title("Классификатор пресс-релизов ЦБ с предсказанием будущей ключевой ставки")

# Раздел "Описание проекта"
st.header("Описание проекта")

st.write("""ЦБ каждый раз после заседания по ключевой ставке на сайте публикует пресс-релизы,
в которых рассказывается про состояние экономики, инфляцию, спрос на продукты,
услуги и т.д. и объясняет причину изменения/не изменения ставки. Задача состоит
в том, чтобы по семантике текста понять, что будет происходить с ключевой ставкой
на следующем заседании: ЦБ её поднимет, опустит или оставит неизменной.
Мы создали классификатор, который разделяет тексты релизов на 3 класса: -1
(ставка опустится), 0 (останется неизменной), 1 (ставку повысят).""")

st.write("""Для того, чтобы протестировать модель, вы можете загрузить свой
файл с данными. Файл должен содержать столбец 'release' с текстами и столбец
'target_categorial', где -1 означает снижение ставки, 0 сохранение ставки,
1 повышение ставки.""")

# Раздел "Загрузка данных"
st.header("Загрузка данных")

# Установка начального состояния переменной для загрузки внешних данных
st.session_state['other_data'] = False

# Загрузка стандартного файла данных
data: pd.DataFrame = pd.read_csv('./data/cbr-press-releases.csv')
st.session_state['data'] = data

# Обработка пользовательской загрузки файла
if upload_file := st.file_uploader("Выберите файл с данными", type='csv'):
    data = pd.read_csv(upload_file)
    st.session_state['other_data'] = True

    logger.info(
        "пользовательски файл: %s загружен.",
        upload_file.name
    )

    # Проверка наличия необходимых столбцов в загруженном файле
    columns: set = set(data.columns)

    if 'release' not in columns:
        logger.error("Файл не содержит столбца 'release'.")
        st.error("Ошибка: Файл должен содержать столбец 'release' с текстами.")
        st.session_state['other_data'] = False

    if 'target_categorial' not in columns:
        logger.error("Файл не содержит столбца 'target_categorial'.")
        st.error("Ошибка: Файл должен содержать столбец 'target_categorial'.")
        st.session_state['other_data'] = False

    # Обновление данных в сессии при успешной проверке
    if st.session_state['other_data']:
        st.session_state['data'] = data

# Отправка данных на сервер для обработки
try:
    res = asyncio.run(
        client.load_data('/load_data', st.session_state['data'])
    )
except Exception as e:
    logger.error("Ошибка при загрузке данных на сервер: %s", e)
    raise e

logger.info("Данные загружены на сервер.")

# Раздел для отображения загруженных данных
st.subheader("Используемые данные")
st.dataframe(st.session_state.data)
