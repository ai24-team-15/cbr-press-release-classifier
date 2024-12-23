import streamlit as st

from utils import get_vectors, COLORS, preprocessing_release
from data import DATA
from plots import plot_linspace


st.subheader('Представление пресс-релизов в двумерном пространстве')

X_tsne = get_vectors(DATA)
fig = plot_linspace(X_tsne, title='', df=DATA, colors=COLORS)

st.plotly_chart(fig)