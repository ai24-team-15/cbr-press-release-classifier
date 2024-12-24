import streamlit as st

from utils import get_preprocess_texts, get_freq, calc_common_words
from plots import plot_wordcloud_all, plot_wordcloud_per_class

data = st.session_state['data']

texts_neg_class = get_preprocess_texts(data, -1)
texts_zero_class = get_preprocess_texts(data, 0)
texts_pos_class = get_preprocess_texts(data, 1)
texts_all_class = get_preprocess_texts(data)

cnt_words_neg_class = get_freq(texts_neg_class)
cnt_words_zero_class = get_freq(texts_zero_class)
cnt_words_pos_class = get_freq(texts_pos_class)
cnt_words_all_classes = get_freq(texts_all_class)

data = {-1: cnt_words_neg_class, 0: cnt_words_zero_class, 1: cnt_words_pos_class}

common_words = calc_common_words(
    cnt_words_neg_class, 
    cnt_words_zero_class, 
    cnt_words_pos_class
    )

st.subheader('Облако слов для всех классов')

st.pyplot(plot_wordcloud_all(cnt_words_all_classes, ''))

st.subheader('Облака слов с разделением по классам')
st.pyplot(plot_wordcloud_per_class(data, '', common_words))