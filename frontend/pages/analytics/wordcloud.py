import pickle
import pandas as pd
import streamlit as st

from tools.utils import get_data_for_wordclouds
from tools.plots import plot_wordcloud_all, plot_wordcloud_per_class
from tools.config import log as logger


# Загрузка данных в session_state или чтение из файла
if 'data' not in st.session_state:
    data: pd.DataFrame = pd.read_csv('./data/cbr-press-releases.csv')
    st.session_state['data'] = data
    st.session_state['other_data'] = False

logger.info("Начало построения облака слов.")

# Подготовка данных для облаков слов
if st.session_state['other_data']:
    data_wordclouds: dict = get_data_for_wordclouds(st.session_state['data'])
else:
    with open('./data/data_wordclouds.pkl', 'rb') as f:
        data_wordclouds: dict = pickle.load(f)

# Извлечение данных для визуализации
wordcloud_data: dict = data_wordclouds['data']
common_words: set[str] = data_wordclouds['common_words']
cnt_words_all_classes: dict = data_wordclouds['cnt_words_all_classes']

# Отображение облака слов для всех классов
st.subheader('Облако слов для всех классов')
st.pyplot(plot_wordcloud_all(cnt_words_all_classes, ''))

# Отображение облаков слов для каждого класса
st.subheader('Облака слов с разделением по классам')
st.pyplot(plot_wordcloud_per_class(wordcloud_data, common_words))
logger.info('Облака слов построены.')

# Описание метода облака слов
big_text: str = """
Облако слов — это метод визуализации, который позволяет быстро оценить частотность слов в тексте.
В нашем проекте все слова разделены на облака в соответствии с решениями ЦБ по сохранению,
увеличению или снижению ключевой ставки. Слова с позитивным или нейтральным оттенком чаще встречаются
при снижении или сохранении ставки. При увеличении ключевой ставки ЦБ чаще всего встречаются слова, связанные
с инфляцией, ростом, потреблением и рисками. Популярность данных слов в пресс-релизах ЦБ как раз связана с текущей
экономической ситуацией в России, где происходят существенные вливания денежных средств в
ОПК в результате чего появляется излишний спрос в экономике, что становится, с учетом других факторов
(курс валют, низкая безработица и пр.) причиной роста цен (инфляции).
"""

# Отображение текстового описания в приложении Streamlit
st.write(big_text)
