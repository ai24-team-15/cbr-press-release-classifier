import logging

import streamlit as st
import pandas as pd

from config import configure_logging


configure_logging()
logger = logging.getLogger(__name__)

st.title("Классификатор пресс-релизов ЦБ с предсказанием будущей ключевой ставки")

st.header("Описание проекта")

st.write("""ЦБ каждый раз после заседания по ключевой ставке на сайте публикует пресс-релизы, 
в которых рассказывается про состояние экономики, инфляцию, спрос на продукты, 
услуги и т.д. и объясняет причину изменения/не изменения ставки. Задача состоит 
в том, чтобы по семантике текста понять, что будет происходить с ключевой ставкой
после на следующем заседании: ЦБ ее поднимет, опустит или оставит неизменной. 
Мы создали классификатор, который разделяет тексты релизов на 3 класса: -1 
(ставка опустится), 0 (останется неизменной), 1 (ставку повысят).""")

st.write("""Для того, чтобы протестировать модель, вы можете загрузить свой 
файл с данным. Файл должен содержать столбец 'release' с текстами и столбец 
'target_categorial', где -1 означает снижение ставки, 0 сохранение ставки, 
1 повышение ставки.""")

st.header("Загрузка данных")

if upload_file:= st.file_uploader("Выберите файл с данными", type='csv'):
    DATA = pd.read_csv(upload_file)

    logger.info(
        "Файл: %s загружен.",
        upload_file.name
    )

    columns = set(DATA.columns)

    if 'release' not in columns:
        logger.error("Файл не содержит столбца 'release'.")
        st.error("Ошибка: Файл должен содержать столбец 'release' с текстами.")
        DATA = pd.read_csv('../data/cbr-press-releases.csv')

    if 'target_categorial' not in columns:
        logger.error("Файл не содержит столбца 'target_categorial'.")
        st.error("Ошибка: Файл должен содержать столбец 'target_categorial'.")
        DATA = pd.read_csv('../data/cbr-press-releases.csv')

else:
    DATA = pd.read_csv('../data/cbr-press-releases.csv')

DATA['target_categorial_name'] = DATA.target_categorial.map(
        {
            -1: 'Снижение ставки', 
            1: 'Повышение ставки', 
            0: 'Сохранение ставки'
        }
    )

st.session_state['data'] = DATA

st.subheader("Используемые данные")
st.dataframe(st.session_state.data)
