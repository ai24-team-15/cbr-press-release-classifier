import streamlit as st
import logging
import pickle 
import pandas as pd

from tools.utils import get_preprocess_texts, get_freq, calc_common_words, get_data_for_wordclouds
from tools.plots import plot_wordcloud_all, plot_wordcloud_per_class
from tools.config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

if 'data' not in st.session_state:
    data = pd.read_csv('./data/cbr-press-releases.csv')
    st.session_state['data'] = data
    st.session_state['other_data'] = False

logger.info("Начало построения облака слов.")
if st.session_state['other_data'] == True:
    data_wordclouds = get_data_for_wordclouds(st.session_state['data'])

else:
    with open('./data/data_wordclouds.pkl', 'rb') as f:
        data_wordclouds = pickle.load(f)

data = data_wordclouds['data']


common_words = data_wordclouds['common_words']
cnt_words_all_classes = data_wordclouds['cnt_words_all_classes']

st.subheader('Облако слов для всех классов')

st.pyplot(plot_wordcloud_all(cnt_words_all_classes, ''))

st.subheader('Облака слов с разделением по классам')
st.pyplot(plot_wordcloud_per_class(data, '', common_words))
logger.info('Облака слов построены.')


big_text = """
Облако слов — это метод визуализации, который позволяет быстро оценить частотность слов в тексте.  
В нашем проекте все слова разделены на облака в соответствии с решениями ЦБ по сохранению, увеличению или снижению ключевой ставки.    
Слова с позитивным или нейтральным оттенком чаще встречаются при снижении или сохранении ставки.  
При увеличении ключевой ставки ЦБ чаще всего встречаются слова, связанные с инфляцией, ростом, потреблением и рисками. Популярность данных слов в пресс-релизах ЦБ как раз связана с текущей экономической ситуацией в России, где происходят существенные вливания денежных средств в ОПК в результате чего появляется излишний спрос в экономике, что становится, с учетом других факторов (курс валют, низкая безработица и пр.) причиной роста цен (инфляции).
"""
st.write(big_text)
