import streamlit as st
import pandas as pd
from plotly import express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from plots import plot_pie, plot_dinamic, \
    plot_len_text, plot_boxplot

COLORS = {
    'Снижение ставки': '#4D6D7F',
    'Сохранение ставки': '#1A4E1A',
    'Повышение ставки': '#A03B2A',
    -1: '#4D6D7F',
    1: '#1A4E1A',
    0: '#A03B2A'
}

st.title("Предсказание ставки центрального банка")

st.header("Исследовательский анализ данных")

df = pd.read_csv('../data/cbr-press-releases.csv')

df['target_categorial_name'] = df.target_categorial.map(
        {
            -1: 'Снижение ставки', 
            1: 'Повышение ставки', 
            0: 'Сохранение ставки'
        }
    )

data = df.groupby('target_categorial_name').title.count()
data = data / data.sum()
data = data.reset_index()

data = data.rename(
    columns={
        'target_categorial_name': 'Решение по ключевой ставке', 
        'title': 'Доля'
        }
    )

st.plotly_chart(plot_pie(data, COLORS))

data = df.copy()
data['rate'] = data['rate'].shift(1)

st.plotly_chart(plot_dinamic(data))

# Отображение графика
st.plotly_chart(plot_len_text(df))

# Печать статистики
st.write(f'Средняя длина текстов - {df["release"].str.len().mean():.2f} символов')
st.write(f'Самый длинный текст - {df["release"].str.len().max()} символов')
st.write(f'Самый короткий текст - {df["release"].str.len().min()} символов')

df['release_len'] = df.release.str.len()

# Отображение графика
st.plotly_chart(plot_boxplot(df, COLORS))
