import streamlit as st
import logging
import pandas as pd

from tools.plots import plot_dinamic
from tools.config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

if 'data' in st.session_state:
    data = st.session_state['data'].copy()
else:
    data = pd.read_csv('./data/cbr-press-releases.csv')
    st.session_state['data'] = data.copy()
    st.session_state['other_data'] = False

data['rate'] = data['rate'].shift(1)

logger.info("Начало построения динамики ставки ЦБ.")
st.subheader('Изменение ставки центрального банка')
st.plotly_chart(plot_dinamic(data))
logger.info("График динамики ставки построен.")
