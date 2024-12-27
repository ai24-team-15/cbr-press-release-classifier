import plotly.express as px
from plotly.subplots import make_subplots
from plotly import graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import streamlit as st

def plot_pie(data, colors):
    fig = px.pie(
            data, 
            names='Решение по ключевой ставке', 
            values='Доля', 
            color='Решение по ключевой ставке',
            color_discrete_map=colors
        )

    return fig


def plot_dinamic(data):
    # Создаем фигуру с двумя осями Y
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
            go.Scatter(
                name='Величина ставки',
                x=data['date'] ,
                y=data['rate'],
                # mode='markers',
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

    # Настройка заголовка, меток осей и легенды
    fig.update_layout(
        title='',
        font=dict(size=16),
        xaxis_title='Дата',
        yaxis_title='Ставка / инфляция',
        yaxis2_title='Курс USD'
    )

    return fig


def plot_len_text(data):
    # Создаем фигуру с двумя подграфиками
    fig = make_subplots(
        rows=2, 
        cols=1, 
        row_heights=[0.2, 0.8], 
        shared_xaxes=False,
        vertical_spacing=0.05
    )

    # Добавляем бокс-плот на верхний подграфик
    fig.add_trace(
        go.Box(
            x=data['release'].str.len(),
            orientation='h',
            marker_color='#5975A4',
            showlegend=False
        ),
        row=1, col=1
    )

    # Добавляем гистограмму на нижний подграфик
    fig.add_trace(
        go.Histogram(
            x=data['release'].str.len(),
            marker_color='#5975A4',
            nbinsx=17,
            showlegend=False
        ),
        row=2, col=1
    )

    # Настройка заголовков осей и общего заголовка
    fig.update_layout(
        xaxis_title='Количество символов',
        xaxis2_title='Количество символов',
        yaxis_title='',
        yaxis2_title='Количество наблюдений',
        font=dict(size=12),
    )

    # Удаление заголовка оси Y для верхнего подграфика
    fig.update_xaxes(title_text="", row=1, col=1)
    fig.update_yaxes(title_text="", row=1, col=1)

    return fig

def plot_boxplot(data, colors):
    fig = px.box(
        data, 
        x="target_categorial_name", 
        y="release_len", 
        color="target_categorial_name", 
        color_discrete_map=colors
    )

    # Настройка заголовка, меток осей и легенды
    fig.update_layout(
        font=dict(size=16),
        xaxis_title='Решение по ставке',
        yaxis_title='Длина текста',
    )

    return fig
@st.cache_resource
def plot_wordcloud_all(data: dict, title: str):
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
    plt.suptitle(
        title, 
    )
    ax.imshow(wordcloud)
    return fig

@st.cache_resource
def plot_wordcloud_per_class(data: dict[int, dict], title: str, common_words: set[str]):
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
            ).generate_from_frequencies({k: v for k, v in data[target].items() if k not in common_words})
        
        clouds.append(wordcloud)

    fig, axes = plt.subplots(1, len(data.keys()), figsize=(28,10))

    titles = ['Ставка снизится', 'Ставка не изменится', 'Ставка повысится']
    for ax, cloud, ttl in zip(axes, clouds, titles):
        ax.grid(visible=False)
        ax.axis('off')
        ax.set_title(ttl)
        ax.imshow(cloud)

    return fig


def plot_linspace(X, title: str, df, colors):
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
        marker=dict(size=10, color=colors[1]), 
        )
    fig.add_scatter(
        x=X[neg_index, 0],
        y=X[neg_index, 1], 
        mode='markers', 
        text=df.date.loc[neg_index], 
        name='Понизить',
        marker=dict(size=10, color=colors[-1]), 
        )
    fig.add_scatter(
        x=X[zero_index, 0],
        y=X[zero_index, 1],
        mode='markers', 
        text=df.date.loc[zero_index], 
        name='Сохранить',
        marker=dict(size=10, color=colors[0]), 
        )
    fig.update_layout(
        showlegend=True, 
        height=650, 
        width=650, 
        margin=dict(l=20,r=20,b=10,t=40),
        title=title,
        title_font=dict(size=18, color='black', weight='bold'),
        title_x=0.5,
        )
    
    return fig
