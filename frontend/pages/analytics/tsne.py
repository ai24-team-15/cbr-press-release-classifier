import pickle
import streamlit as st
import logging
import pandas as pd

from tools.utils import get_vectors, COLORS, preprocessing_release
from tools.plots import plot_linspace
from tools.config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

st.subheader('Представление пресс-релизов в двумерном пространстве')

logger.info('Начало построения графика tsne.')
if 'data' in st.session_state:
    data = st.session_state['data']
else:
    data = pd.read_csv('./data/cbr-press-releases.csv')
    st.session_state['data'] = data
    st.session_state['other_data'] = False

if st.session_state['other_data']:
    data['corpus'] = data.release.map(preprocessing_release)
    X_tsne = get_vectors(data)
else:
    with open('./data/data_tsne.pkl', 'rb') as f:
        X_tsne = pickle.load(f)

fig = plot_linspace(X_tsne, title='', df=data, colors=COLORS)

st.plotly_chart(fig)
logger.info('График tsne построен.')
big_text = """
Это график, который показывает распределение пресс-релизов в двумерном пространстве с использованием метода t-SNE. t-SNE (t-distributed stochastic neighbor embedding) — это алгоритм, снижения размерности данных используемый для визуализации многомерных данных в двумерном пространстве. t-SNE способен выявлять нелинейные зависимости между данными, сокращает время обработки данных, увеличивает точность модели машинного обучения и помогает избегать переобучения. 
Цвета точек на графике обозначают различные категории пресс-релизов. Все точки на визуализации были распределены на кластеры. Кластеры указывают на группы схожих объектов (преобразованных текстов в вектора), которые в данном случае привели к решениям ЦБ по сохранению, увеличению или снижению ключевой ставки.  
Как видим на графике:
- точки, находящиеся рядом, имеют близкие даты выхода пресс-релизов ЦБ;
- точки разбиты на два больших кластера пресс-релизы до 2018 года и после. 
- до 2018 года скученность точек указывает на то, что кластеры (снижения, сохранения ставки) имеют большую схожесть чем после 2018 года. 
- большие расстояния между точками после 2018 года демонстрируют меньшую схожесть, что скорее всего связано с менее стабильной экономической ситуацией в стране и более негативным описательным составом этих событий в содержании пресс-релизов.
"""
st.write(big_text)
