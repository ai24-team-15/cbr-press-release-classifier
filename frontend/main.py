import os
import asyncio
import pickle

import streamlit as st
import pandas as pd

from tools.utils import download_file, get_data_for_wordclouds, \
    get_vectors, preprocessing_release
from tools.config import log as logger


# Конфигурация страницы Streamlit
st.set_page_config(
    page_title="Checkpoint 4",
)

# Проверяем наличие файла с данными. Если его нет, загружаем из S3
if not os.path.exists('./data/cbr-press-releases.csv'):
    logger.info("Загрузка данных из S3.")
    try:
        asyncio.run(
            download_file(
                'https://storage.yandexcloud.net/cbr-press-release-classifier/cbr-press-releases.csv',
                './data/cbr-press-releases.csv'
            )
        )
    except Exception as e:
        logger.error("Ошибка при загрузке данных из S3: %s", e)
        raise e
    logger.info('Загрузка данных из S3 завершена.')

# Загружаем данные пресс-релизов
data = pd.read_csv('./data/cbr-press-releases.csv')

# Проверяем наличие файла с данными для облаков слов. Если его нет, создаём
if not os.path.exists('./data/data_wordclouds.pkl'):
    logger.info('Подготовка данных для построения облаков слов.')
    data_wordclouds = get_data_for_wordclouds(data)
    with open('./data/data_wordclouds.pkl', 'wb') as f:
        pickle.dump(data_wordclouds, f)
    logger.info('Подготовка данных для построения облаков слов завершена.')

# Проверяем наличие файла с данными для t-SNE. Если его нет, создаём
if not os.path.exists('./data/data_tsne.pkl'):
    logger.info('Подготовка данных для построения t-SNE.')
    data['corpus'] = data['release'].map(preprocessing_release)
    X_tsne = get_vectors(data)
    with open('./data/data_tsne.pkl', 'wb') as f:
        pickle.dump(X_tsne, f)
    logger.info('Подготовка данных для построения t-SNE завершена.')

# Определяем страницы приложения
# Главная страница
title_page = st.Page(
    "pages/title.py",
    title="О проекте",
)

# Страницы исследовательского анализа
pie_page = st.Page(
    "pages/analytics/pie.py",
    title="Распределение решений",
)

dinamic_page = st.Page(
    "pages/analytics/dinamic.py",
    title="Динамика ставки",
)

length_text_page = st.Page(
    "pages/analytics/length_text.py",
    title="Анализ длины текстов",
)

wordcloud_page = st.Page(
    "pages/analytics/wordcloud.py",
    title="Облака слов",
)

tsne_page = st.Page(
    "pages/analytics/tsne.py",
    title="t-SNE визуализация",
)

# Страницы машинного обучения
fit_page = st.Page(
    "pages/machine_learning/fit.py",
    title="Обучение модели",
)

predict_page = st.Page(
    "pages/machine_learning/predict.py",
    title="Предсказание",
)

# Настройка навигации между страницами
pg = st.navigation(
    {
        "Главная": [title_page],
        "Исследовательский анализ": [
            pie_page, dinamic_page,
            length_text_page,
            wordcloud_page,
            tsne_page
        ],
        "Машинное обучение": [fit_page, predict_page],
    }
)

# Запуск выбранной страницы
pg.run()
