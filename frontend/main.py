import streamlit as st
import pandas as pd
from plotly import express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE

from plots import plot_pie, plot_dinamic, \
    plot_len_text, plot_boxplot, plot_wordcloud_all, \
        plot_wordcloud_per_class, plot_linspace
from utils import get_preprocess_texts, get_freq, \
    preprocessing_release, calc_common_words, get_vectors

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

st.subheader('Распределение решений по ключевой ставке')

st.plotly_chart(plot_pie(data, COLORS))

data = df.copy()
data['rate'] = data['rate'].shift(1)

st.subheader('Изменение ставки центрального банка')
st.plotly_chart(plot_dinamic(data))

st.subheader('Распределение длин текстов релизов')
st.plotly_chart(plot_len_text(df))

# Печать статистики
st.write(f'Средняя длина текстов - {df["release"].str.len().mean():.2f} символов')
st.write(f'Самый длинный текст - {df["release"].str.len().max()} символов')
st.write(f'Самый короткий текст - {df["release"].str.len().min()} символов')

df['release_len'] = df.release.str.len()

st.subheader('Распределение длин текстов релизов с разделением по классам')
st.plotly_chart(plot_boxplot(df, COLORS))

texts_neg_class = get_preprocess_texts(df, -1)
texts_zero_class = get_preprocess_texts(df, 0)
texts_pos_class = get_preprocess_texts(df, 1)
texts_all_class = get_preprocess_texts(df)

cnt_words_neg_class = get_freq(texts_neg_class)
cnt_words_zero_class = get_freq(texts_zero_class)
cnt_words_pos_class = get_freq(texts_pos_class)
cnt_words_all_classes = get_freq(texts_all_class)

data = {-1: cnt_words_neg_class, 0: cnt_words_zero_class, 1: cnt_words_pos_class}

common_words = calc_common_words(
    cnt_words_neg_class, 
    cnt_words_zero_class, 
    cnt_words_pos_class
    )

st.subheader('Облако слов для всех классов')

st.pyplot(plot_wordcloud_all(cnt_words_all_classes, ''))

st.subheader('Облака слов с разделением по классам')
st.pyplot(plot_wordcloud_per_class(data, '', common_words))

df['corpus'] = df.release.apply(preprocessing_release)

X_tsne = get_vectors(df)

st.subheader('Представление пресс-релизов в двумерном пространстве')
fig = plot_linspace(X_tsne, title='', df=df, colors=COLORS)

st.plotly_chart(fig)
