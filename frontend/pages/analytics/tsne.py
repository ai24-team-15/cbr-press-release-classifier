import streamlit as st

from utils import get_vectors, COLORS, preprocessing_release
from plots import plot_linspace


st.subheader('Представление пресс-релизов в двумерном пространстве')

data = st.session_state['data']
data['corpus'] = data.release.map(preprocessing_release)

X_tsne = get_vectors(data)
fig = plot_linspace(X_tsne, title='', df=data, colors=COLORS)

st.plotly_chart(fig)