import streamlit as st

from plots import plot_pie
from utils import COLORS
from data import DATA

st.subheader('Распределение решений по ключевой ставке')

df = DATA.groupby('target_categorial_name').title.count()
df = df / df.sum()
df = df.reset_index()

df = df.rename(
    columns={
        'target_categorial_name': 'Решение по ключевой ставке', 
        'title': 'Доля'
        }
    )

st.plotly_chart(plot_pie(df, COLORS))
