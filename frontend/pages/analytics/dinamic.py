import streamlit as st

from data import DATA
from plots import plot_dinamic

data = DATA.copy()

data['rate'] = data['rate'].shift(1)

st.subheader('Изменение ставки центрального банка')
st.plotly_chart(plot_dinamic(data))