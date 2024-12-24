import streamlit as st

from plots import plot_dinamic

data = st.session_state['data'].copy()

data['rate'] = data['rate'].shift(1)

st.subheader('Изменение ставки центрального банка')
st.plotly_chart(plot_dinamic(data))