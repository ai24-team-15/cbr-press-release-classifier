from typing import Dict, Set, List, Any
import plotly.express as px
from plotly.subplots import make_subplots
from plotly import graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics import auc, roc_curve, confusion_matrix
from sklearn.preprocessing import label_binarize

from tools.utils import CATEGORIAL_NAMES, COLORS


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


def create_roc_curve(
        y_true: List[int],
        y_score: np.array,
        classes: List[int],
        model_name: str
) -> List[go.Scatter]:
    """
    Создает ROC-кривые для многоклассовой классификации.

    Параметры:
        y_true (List[int]): Список истинных меток классов.
        y_score (List[List[float]]): Прогнозируемые вероятности для каждого класса.
        classes (List[int]): Список всех уникальных меток классов.
        model_name (str): Название модели, отображаемое в легенде.

    Возвращает:
        List[go.Scatter]: Список объектов Scatter для построения ROC-кривых в Plotly.
    """
    # Бинаризуем истинные метки классов
    y_bin = label_binarize(y_true, classes=classes)

    # Словари для хранения значений FPR, TPR и AUC для каждого класса
    fpr: Dict[int, List[float]] = {}
    tpr: Dict[int, List[float]] = {}
    roc_auc: Dict[int, float] = {}

    # Вычисляем FPR, TPR и AUC для каждого класса
    for i in range(len(classes)):
        fpr[i], tpr[i], _ = roc_curve(y_bin[:, i], y_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    # Создаем список графиков ROC-кривых
    traces: List[go.Scatter] = []
    n_classes = len(classes)
    for i in range(n_classes):
        traces.append(go.Scatter(
            x=fpr[i],  # False Positive Rate для текущего класса
            y=tpr[i],  # True Positive Rate для текущего класса
            mode='lines',  # Линия графика
            # Название класса и AUC
            name=f'{model_name} - {CATEGORIAL_NAMES[classes[i]]} (AUC = {roc_auc[i]:.2f})',
            line={'color': COLORS[classes[i]], 'width': 2}  # Настройка цвета и толщины линии
        ))

    return traces


def plot_confusion_matrix(data: Dict[str, Any]) -> go.Figure:
    """
    Функция для отображения матрицы ошибок для нескольких моделей с использованием Plotly.

    Параметры:
        data (Dict[str, Any]): Словарь, где ключи — это идентификаторы моделей,
                                а значения — это данные с истинными метками ('y_trues')
                                и предсказанными метками ('y_preds').

    Возвращает:
        go.Figure: Визуализация матрицы ошибок с помощью Plotly.
    """
    num_models = len(data)  # Количество моделей

    fig = make_subplots(
            rows=1, cols=num_models,
            subplot_titles=list(data.keys())
        )

    # Обрабатываем каждую модель в словаре data
    for i, (model_id, data_model) in enumerate(data.items()):
        # Вычисляем матрицу ошибок для текущей модели
        cm = confusion_matrix(data_model['y_trues'], data_model['y_preds'])

        # Преобразуем матрицу в DataFrame для удобства
        cm_df = pd.DataFrame(cm, index=['-1', '0', '1'], columns=['-1', '0', '1'])

        cm_df = cm_df.iloc[:, [2, 1, 0]]

        # Добавляем график для каждой модели
        fig.add_trace(go.Heatmap(
            z=cm_df.values,  # Значения для тепловой карты
            x=cm_df.columns,  # Метки по оси X (предсказанные метки)
            y=cm_df.index,  # Метки по оси Y (истинные метки)
            colorscale='Viridis',  # Цветовая схема
            showscale=True,
            name=model_id,  # Название модели в легенде
            text=cm_df.values,  # Значения для отображения в ячейках
            texttemplate='%{text}',  # Шаблон для отображения значений
            textfont={'size': 32, 'color': 'white'}  # Настройки шрифта для текста
        ), row=1, col=i+1)
        fig.update_xaxes(title_text='Предсказанные ответы', row=1, col=i+1)
        if i < 1:
            fig.update_yaxes(title_text='Реальные классы', row=1, col=i+1)

    # Настройки макета для графика
    fig.update_layout(
        showlegend=True  # Показываем легенду для каждой модели
    )

    return fig


def plot_auc(data: Dict[str, Any]) -> go.Figure:
    """
    Строит графики ROC AUC для нескольких моделей в формате сетки.

    Args:
        data (Dict[str, Any]): Словарь, где ключи — идентификаторы моделей (model_id),
                               а значения — данные модели, включающие:
                               - `y_trues`: истинные метки классов,
                               - `y_pred_probas`: вероятности предсказаний.

    Returns:
        go.Figure: График Plotly с сеткой, содержащей ROC-кривые для каждой модели.
    """
    traces = []  # Список для хранения ROC-кривых для каждой модели

    # Генерация ROC-кривых для каждой модели
    for i, (model_id, data_model) in enumerate(data.items()):
        traces.append(
            create_roc_curve(
                data_model['y_trues'],  # Истинные метки классов
                np.array(data_model['y_pred_probas']),  # Предсказанные вероятности
                [-1, 0, 1],  # Классы
                model_id  # Идентификатор модели
            )
        )

    # Создание объекта с сеткой графиков
    fig = make_subplots(
        rows=1, cols=len(traces),  # Одна строка, количество столбцов соответствует числу моделей
        subplot_titles=list(data.keys())  # Заголовки графиков — идентификаторы моделей
    )

    # Добавление графиков в сетку
    for i, trace in enumerate(traces):
        for t in trace:  # Добавляем каждую кривую ROC из текущей модели
            fig.add_trace(t, row=1, col=i + 1)

        # Настройка осей X для каждого графика
        fig.update_xaxes(title_text='False Positive Rate', row=1, col=i + 1)

        # Настройка осей Y только для первого графика
        if i < 1:
            fig.update_yaxes(title_text='True Positive Rate', row=1, col=i + 1)

    # Общие настройки для графика
    fig.update_layout(
        showlegend=True  # Включение легенды
    )

    return fig
