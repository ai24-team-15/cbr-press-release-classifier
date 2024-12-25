import streamlit as st
import logging

from plots import plot_pie
from utils import COLORS
from config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

st.subheader('Распределение решений по ключевой ставке')
logger.info("Начало построения графиков длин текстов.")

data = st.session_state['data']
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
