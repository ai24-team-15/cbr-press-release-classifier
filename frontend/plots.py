import plotly.express as px
from plotly.subplots import make_subplots
from plotly import graph_objects as go

def plot_pie(data, colors):
    fig = px.pie(
            data, 
            names='Решение по ключевой ставке', 
            values='Доля', 
            color='Решение по ключевой ставке',
            color_discrete_map=colors
        )

    # Настройка заголовка, меток осей и легенды
    fig.update_layout(
        title='Распределение решений по ключевой ставке',
        title_x=0.3,
        font=dict(size=16),
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
        title='Изменение ставки центрального банка',
        title_x=0.3,
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
        title_text='Распределение длин текстов релизов',
        title_x=0.3,
        title_font_size=16,
        title_font=dict(weight='bold')
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
        title='Распределение длин тесктов релизов',
        title_x=0.3,
        font=dict(size=16),
        xaxis_title='Решение по ставке',
        yaxis_title='Длина текста',
    )

    return fig
