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