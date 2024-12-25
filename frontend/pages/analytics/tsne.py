import streamlit as st
import logging

from utils import get_vectors, COLORS, preprocessing_release
from plots import plot_linspace
from config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

st.subheader('Представление пресс-релизов в двумерном пространстве')

logger.info('Начало построения графика tsne.')
data = st.session_state['data']
data['corpus'] = data.release.map(preprocessing_release)

X_tsne = get_vectors(data)
fig = plot_linspace(X_tsne, title='', df=data, colors=COLORS)

st.plotly_chart(fig)
logger.info('График tsne построен.')