import re
from typing import Union
from collections import Counter

import pandas as pd
import matplotlib.pyplot as plt
import nltk
from pymystem3 import Mystem
from wordcloud import WordCloud
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE


def preprocessing_release(text: str) -> list[str]:
    stop_words = set(nltk.corpus.stopwords.words('russian'))
    regex = re.compile('[^а-я ]')
    mystem = Mystem()

    text = text.lower()
    text = regex.sub(' ', text)
    text = filter(lambda w: not w.isspace(), mystem.lemmatize(text))
    text = list(filter(lambda w: w not in stop_words and len(w) != 1, text))
    return text

@st.cache_data
def get_preprocess_texts(df: pd.DataFrame, class_cat: Union[int, None]=None) -> list[str]:
    if class_cat is None:
        df = df.release
    else:
        df = df.loc[df.target_categorial == class_cat, 'release']
        
    texts_raw = ' '.join(df.to_list())
    texts = preprocessing_release(texts_raw)
    return texts

@st.cache_data
def get_freq(texts: list[str]) -> dict[str, float]:
    cnt_words = Counter(texts)
    num_words = sum(cnt_words.values())
    cnt_words = {k: v / num_words for k, v in cnt_words.items()}
    cnt_words = dict(sorted(cnt_words.items(), key=lambda w: -w[1]))
    return cnt_words

@st.cache_data
def calc_common_words(*cnt_words_dic: dict, top:int=15) -> set[str]:
    result = set(list(cnt_words_dic[0].keys())[:top])

    for dic in cnt_words_dic[1:]:
        result.intersection_update(set(list(dic.keys())[:top]))
    
    return result

@st.cache_resource
def get_vectors(df):
    vec = TfidfVectorizer(analyzer=lambda x: x)
    X = vec.fit_transform(df.corpus)

    tsne = TSNE(n_components=2, random_state=42)
    X_tsne = tsne.fit_transform(X.toarray())

    return X_tsne
