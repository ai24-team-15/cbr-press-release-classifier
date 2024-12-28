from typing import Dict, Set
import plotly.express as px
from plotly.subplots import make_subplots
from plotly import graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import streamlit as st
import pandas as pd
import numpy as np


def plot_pie(data: pd.DataFrame, colors: Dict[str, str]) -> go.Figure:
    """
    Построение круговой диаграммы.

    :param data: DataFrame с данными для визуализации.
    :param colors: Словарь с цветовыми значениями для категорий.
    :return: Объект Figure с круговой диаграммой.
    """
    fig = px.pie(
        data,
        names='Решение по ключевой ставке',
        values='Доля',
        color='Решение по ключевой ставке',
        color_discrete_map=colors
    )
    return fig


def plot_dinamic(data: pd.DataFrame) -> go.Figure:
    """
    Построение графика динамики с двумя осями Y.

    :param data: DataFrame с колонками date, rate, inflation, usd.
    :return: Объект Figure с динамическим графиком.
    """
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            name='Величина ставки',
            x=data['date'],
            y=data['rate'],
            marker_color='red',
        ),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(
            name='Инфляция',
            x=data['date'],
            y=data['inflation'],
            marker_color='green'
        ),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(
            name='Курс USD',
            x=data['date'],
            y=data['usd'],
            marker_color='blue'
        ),
        secondary_y=True
    )

    fig.update_layout(
        title='',
        font={'size': 16},
        xaxis_title='Дата',
        yaxis_title='Ставка / инфляция',
        yaxis2_title='Курс USD'
    )

    return fig


def plot_len_text(data: pd.DataFrame) -> go.Figure:
    """
    Построение графика распределения длины текстов.

    :param data: DataFrame с колонкой release (тексты для анализа).
    :return: Объект Figure с бокс-плотом и гистограммой.
    """
    fig = make_subplots(
        rows=2,
        cols=1,
        row_heights=[0.2, 0.8],
        shared_xaxes=False,
        vertical_spacing=0.05
    )

    fig.add_trace(
        go.Box(
            x=data['release'].str.len(),
            orientation='h',
            marker_color='#5975A4',
            showlegend=False
        ),
        row=1, col=1
    )

    fig.add_trace(
        go.Histogram(
            x=data['release'].str.len(),
            marker_color='#5975A4',
            nbinsx=17,
            showlegend=False
        ),
        row=2, col=1
    )

    fig.update_layout(
        xaxis_title='Количество символов',
        xaxis2_title='Количество символов',
        font={'size': 12},
    )

    fig.update_xaxes(title_text="", row=1, col=1)
    fig.update_yaxes(title_text="", row=1, col=1)

    return fig


def plot_boxplot(data: pd.DataFrame, colors: Dict[str, str]) -> go.Figure:
    """
    Построение бокс-плота для категорий.

    :param data: DataFrame с колонками target_categorial_name и release_len.
    :param colors: Словарь с цветовыми значениями для категорий.
    :return: Объект Figure с бокс-плотом.
    """
    fig = px.box(
        data,
        x="target_categorial_name",
        y="release_len",
        color="target_categorial_name",
        color_discrete_map=colors
    )

    fig.update_layout(
        font={'size': 16},
        title={'text': 'Длина текста по категориям'},
        xaxis_title='Решение по ставке',
        yaxis_title='Длина текста',
    )

    return fig


@st.cache_resource
def plot_wordcloud_all(data: Dict[str, int], title: str) -> plt.Figure:
    """
    Построение облака слов для всех данных.

    :param data: Словарь с частотностью слов.
    :param title: Заголовок графика.
    :return: Объект Figure с облаком слов.
    """
    fig, ax = plt.subplots()
    wordcloud = WordCloud(
        width=1200,
        height=1200,
        random_state=42,
        background_color='white',
        max_words=50,
        contour_width=2,
        contour_color='black'
    ).generate_from_frequencies(data)

    ax.grid(visible=False)
    ax.axis('off')
    plt.suptitle(title)
    ax.imshow(wordcloud)
    return fig


@st.cache_resource
def plot_wordcloud_per_class(
        data: Dict[int, Dict[str, int]],
        common_words: Set[str]
) -> plt.Figure:
    """
    Построение облаков слов по категориям.

    :param data: Словарь с частотностью слов для каждой категории.
    :param title: Заголовок графика.
    :param common_words: Множество слов, которые нужно исключить из облаков.
    :return: Объект Figure с облаками слов по категориям.
    """
    clouds = []
    targets = data.keys()
    for target in targets:
        wordcloud = WordCloud(
            width=1200,
            height=1200,
            random_state=42,
            background_color='white',
            max_words=50,
            contour_width=2,
            contour_color='black'
        ).generate_from_frequencies({
            k: v for k, v in data[target].items() if k not in common_words
        })
        clouds.append(wordcloud)

    fig, axes = plt.subplots(1, len(data.keys()), figsize=(28, 10))

    titles = ['Ставка снизится', 'Ставка не изменится', 'Ставка повысится']
    for ax, cloud, ttl in zip(axes, clouds, titles):
        ax.grid(visible=False)
        ax.axis('off')
        ax.set_title(ttl)
        ax.imshow(cloud)

    return fig


def plot_linspace(
        X: np.ndarray,
        title: str,
        df: pd.DataFrame,
        colors: Dict[int, str]
) -> go.Figure:
    """
    Построение двумерного распределения точек.

    :param X: Матрица координат точек.
    :param title: Заголовок графика.
    :param df: DataFrame с колонкой target_categorial.
    :param colors: Словарь с цветовыми значениями для категорий.
    :return: Объект Figure с распределением точек.
    """
    pos_index = df[df.target_categorial == 1].index
    neg_index = df[df.target_categorial == -1].index
    zero_index = df[df.target_categorial == 0].index

    fig = go.Figure()

    fig.add_scatter(
        x=X[pos_index, 0],
        y=X[pos_index, 1],
        mode='markers',
        text=df.date.loc[pos_index],
        name='Повысить',
        marker={'size': 10, 'color': colors[1]},
    )

    fig.add_scatter(
        x=X[neg_index, 0],
        y=X[neg_index, 1],
        mode='markers',
        text=df.date.loc[neg_index],
        name='Понизить',
        marker={'size': 10, 'color': colors[-1]},
    )

    fig.add_scatter(
        x=X[zero_index, 0],
        y=X[zero_index, 1],
        mode='markers',
        text=df.date.loc[zero_index],
        name='Сохранить',
        marker={'size': 10, 'color': colors[0]},
    )

    fig.update_layout(
        showlegend=True,
        height=650,
        width=650,
        margin={'l': 20, 'r': 20, 'b': 10, 't': 40},
        title=title,
        title_font={'size': 18, 'color': 'black', 'weight': 'bold'},
        title_x=0.5,
    )

    return fig
