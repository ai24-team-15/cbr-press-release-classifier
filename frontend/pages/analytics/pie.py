import streamlit as st
import logging
import pandas as pd

from plots import plot_pie
from utils import COLORS, CATEGORIAL_NAMES
from config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

st.subheader('Распределение решений по ключевой ставке')
logger.info("Начало построения графиков длин текстов.")
if 'data' in st.session_state:
    data = st.session_state['data']
else:
    data = pd.read_csv('./data/cbr-press-releases.csv')
    st.session_state['data'] = data
    st.session_state['other_data'] = False

if 'target_categorial_name' not in data.columns:
    data['target_categorial_name'] = data.target_categorial.map(CATEGORIAL_NAMES)

df = data.groupby('target_categorial_name').title.count()
df = df / df.sum()
df = df.reset_index()

df = df.rename(
    columns={
        'target_categorial_name': 'Решение по ключевой ставке', 
        'title': 'Доля'
        }
    )

st.plotly_chart(plot_pie(df, COLORS))
logger.info("Графики длин текстов построены.")
