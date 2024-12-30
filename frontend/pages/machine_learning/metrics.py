import asyncio

import streamlit as st

from tools.api import client
from tools.plots import plot_confusion_matrix, plot_auc
from tools.utils import calc_metrics

st.header('Оценка моделей')

# Получаем список моделей
models = asyncio.run(client.get_models('/get_models'))

# Список id моделей
model_ids = [model['model_id'] for model in models]

# Список описания моделей
model_descriptions = [model['description'] for model in models]

# Выбор моделей для сравнения
selected_models = st.multiselect('Выберите модели для сравнения', model_ids, max_selections=2)

# Добавляем отступ до кнопки
for i in range(7):
    st.write(' ')

# Кнопка для запуска расчета метрик
if st.button('Получить метрики'):
    traces = []  # Список для хранения графиков ROC-кривых
    data = {}  # Словарь для хранения данных о метриках моделей

    # Запрашиваем метрики для каждой выбранной модели
    for model_id in selected_models:
        # Асинхронный вызов API для расчета метрик модели
        data[model_id] = asyncio.run(client.calc_metrics(model_id))

    # Отображаем заголовок для матрицы ошибок
    st.subheader('Матрица ошибок')

    # Генерируем график матрицы ошибок для всех моделей
    fig = plot_confusion_matrix(data)
    # Отображаем график матрицы ошибок в Streamlit
    st.plotly_chart(fig, use_container_width=True)
    # Объяснение пользователю, что показывают матрицы ошибок
    st.write('Можем увидеть какие классы модель чаще всего путает между собой')

    # Отображаем заголовок для таблицы метрик классификации
    st.subheader('Таблица основных метрик классификации')
    # Вычисляем таблицу метрик для всех моделей
    df = calc_metrics(data)
    # Отображаем таблицу метрик в Streamlit
    st.dataframe(df)

    # Отображаем заголовок для ROC-кривых
    st.subheader('ROC-кривые для каждого класса')
    # Генерируем график ROC-кривых для всех моделей
    fig = plot_auc(data)
    # Отображаем график ROC-кривых в Streamlit
    st.plotly_chart(fig, use_container_width=True)
