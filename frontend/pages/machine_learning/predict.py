import asyncio

import streamlit as st
import pandas as pd

from tools.api import client

st.header('Прогнозирование Решения ЦБ')

models = asyncio.run(
    client.get_models('/get_models')
)

model_ids = [model['model_id'] for model in models]

model_id = st.radio('Выберите модель', model_ids)

st.subheader('Выбрана модель:')
for model in models:
    if model_id == model['model_id']:
        for key in model:
            if key == 'hyperparameters':
                if len(model[key]) > 0:
                    st.markdown(f'`{key}`:')
                for k in model[key]:
                    st.markdown(f'* `{k}`: {model[key][k]}') 
            else:
                st.markdown(f'`{key}`: {model[key]}')

source = st.radio("Данные для предсказания", 
         ["Ввести текст пресс-релиза", 
          "Загрузить txt файл", 
          "Использовать последний пресс-релиз"])

release = None
last_release = pd.read_csv('./data/cbr-press-releases.csv').tail(1)
if source == "Ввести текст пресс-релиза":
    release = st.text_input('Введите текст пресс-релиза')

elif source == "Загрузить txt файл":
    file = st.file_uploader('Загрузите txt файл с текстом пресс-релиза', type='txt')
    if file:
        release = file.read().decode("utf-8")

elif source == "Использовать последний пресс-релиз":
    release = last_release['release'].values[0]

if release:
    last_release['release'] = release
    st.subheader('Текущий текст пресс-релиза')
    st.text_area('', release, height=200)


if st.button('Получить предсказание'):
    prediction = asyncio.run(
        client.predict('/predict', model_id=model_id)
    )

    st.subheader('Предсказание модели')
    if prediction['predict'] == -1:
        st.write('На следующем заседании ставка будет снижена.')
    elif prediction['predict'] == 0:
        st.write('На следующем заседании ставка будет сохранена.')
    else:
        st.write('На следующем заседании ставка будет повышена.')
