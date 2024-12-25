import streamlit as st
import logging

from plots import plot_dinamic
from config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

data = st.session_state['data'].copy()

data['rate'] = data['rate'].shift(1)

logger.info("Начало построения динамики ставки ЦБ.")
st.subheader('Изменение ставки центрального банка')
st.plotly_chart(plot_dinamic(data))
logger.info("График динамики ставки построен.")
