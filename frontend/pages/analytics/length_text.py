import streamlit as st

from data import DATA
from utils import COLORS
from plots import plot_len_text, plot_boxplot

st.subheader('Распределение длин текстов релизов')
st.plotly_chart(plot_len_text(DATA))

# Печать статистики
st.write(f'Средняя длина текстов - {DATA["release"].str.len().mean():.2f} символов')
st.write(f'Самый длинный текст - {DATA["release"].str.len().max()} символов')
st.write(f'Самый короткий текст - {DATA["release"].str.len().min()} символов')

DATA['release_len'] = DATA.release.str.len()

st.subheader('Распределение длин текстов релизов с разделением по классам')
st.plotly_chart(plot_boxplot(DATA, COLORS))