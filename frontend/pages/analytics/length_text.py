import streamlit as st
import logging
import pandas as pd

from utils import COLORS, CATEGORIAL_NAMES
from plots import plot_len_text, plot_boxplot
from config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

st.subheader('Распределение длин текстов релизов')

logger.info("Начало построения графиков длин текстов.")
if 'data' in st.session_state:
    data = st.session_state['data']
else:
    data = pd.read_csv('./data/cbr-press-releases.csv')
    st.session_state['data'] = data
    st.session_state['other_data'] = False

if 'target_categorial_name' not in data.columns:
    data['target_categorial_name'] = data.target_categorial.map(CATEGORIAL_NAMES)

st.plotly_chart(plot_len_text(data))

# Печать статистики
st.write(f'Средняя длина текстов - {data["release"].str.len().mean():.2f} символов')
st.write(f'Самый длинный текст - {data["release"].str.len().max()} символов')
st.write(f'Самый короткий текст - {data["release"].str.len().min()} символов')

data['release_len'] = data.release.str.len()

st.subheader('Распределение длин текстов релизов с разделением по классам')
st.plotly_chart(plot_boxplot(data, COLORS))
logger.info("Графики длин текстов построены.")
