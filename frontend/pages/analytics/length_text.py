import streamlit as st
import logging

from utils import COLORS
from plots import plot_len_text, plot_boxplot
from config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

st.subheader('Распределение длин текстов релизов')

logger.info("Начало построения графиков длин текстов.")
data = st.session_state['data']
st.plotly_chart(plot_len_text(data))

# Печать статистики
st.write(f'Средняя длина текстов - {data["release"].str.len().mean():.2f} символов')
st.write(f'Самый длинный текст - {data["release"].str.len().max()} символов')
st.write(f'Самый короткий текст - {data["release"].str.len().min()} символов')

data['release_len'] = data.release.str.len()

st.subheader('Распределение длин текстов релизов с разделением по классам')
st.plotly_chart(plot_boxplot(data, COLORS))
logger.info("Графики длин текстов построены.")
