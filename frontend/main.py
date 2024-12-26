import os
import logging
import asyncio

import streamlit as st

from utils import download_file
from config import configure_logging


configure_logging()
logger = logging.getLogger(__name__)

if not os.path.exists('./data/cbr-press-releases.csv'):
    logger.info("Загрузка данных из s3.")
    asyncio.run(
    download_file(
        'https://storage.yandexcloud.net/cbr-press-release-classifier/cbr-press-releases.csv',
        './data/cbr-press-releases.csv'
    ))   
    logger.info('Загрузка данных из s3 завершена.')

title_page = st.Page(
    "pages/title.py",
    title="О проекте", 
)

pie_page = st.Page(
    "pages/analytics/pie.py", 
    title="Распределение решений", 
    # icon=":material/add_circle:"
    )

dinamic_page = st.Page(
    "pages/analytics/dinamic.py", 
    title="Динамика ставки", 
    # icon=":material/add_circle:"
    )

length_text_page = st.Page(
    "pages/analytics/length_text.py", 
    title="Анализ длины текстов", 
    # icon=":material/add_circle:"
    )

wordcloud_page = st.Page(
    "pages/analytics/wordcloud.py", 
    title="Облака слов", 
    # icon=":material/add_circle:"
    )

tsne_page = st.Page(
    "pages/analytics/tsne.py", 
    title="t-SNE визуализация", 
    # icon=":material/add_circle:"
    )

model_page = st.Page(
    "pages/model.py", 
    title="Модель", 
    # icon=":material/delete:"
    )

pg = st.navigation(
    {
        "Главная": [title_page],
        "Исследовательский анализ": [
            pie_page, dinamic_page, 
            length_text_page, 
            wordcloud_page, 
            tsne_page
            ],
        "Модель": [model_page],
    }
)

st.set_page_config(
        page_title="checkpoint 4", 
        # page_icon=":material/edit:"
    )

pg.run()
