import re
from typing import Union
from collections import Counter

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import plotly.offline as pyo
from sklearn.base import BaseEstimator, TransformerMixin
from gensim.models import word2vec
import nltk
from pymystem3 import Mystem
from wordcloud import WordCloud


COLORS = {
    0: '#1A4E1A',
    1: '#A03B2A',
    -1: '#4D6D7F'
}

PARTS_OF_SPEECH = {
    'A': 'прилагательное',
    'ADV': 'наречие',
    'ADVPRO': 'местоименное наречие',
    'ANUM': 'числительное-прилагательное',
    'APRO': 'местоимение-прилагательное',
    'COM': 'часть композита - сложного слова',
    'CONJ': 'союз',
    'INTJ': 'междометие',
    'NUM': 'числительное',
    'PART': 'частица',
    'PR': 'предлог',
    'S': 'существительное',
    'SPRO': 'местоимение-существительное',
    'V': 'глагол',
}


class Word2VecVectorizer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.model = None

    def fit(self, X, y=None):
        self.model = word2vec.Word2Vec(X, vector_size=300, window=3, workers=8)
        return self

    def transform(self, X):
        return np.array([
            np.mean([self.model.wv[w] for w in words if w in self.model.wv]
                    or [np.zeros(self.model.vector_size)], axis=0)
            for words in X
        ])


def preprocessing_release(text: str) -> list[str]:
    stop_words = set(nltk.corpus.stopwords.words('russian'))
    regex = re.compile('[^а-я ]')
    mystem = Mystem()

    text = text.lower()
    text = regex.sub(' ', text)
    text = filter(lambda w: not w.isspace(), mystem.lemmatize(text))
    text = list(filter(lambda w: w not in stop_words and len(w) != 1, text))
    return text


def get_preprocess_texts(df: pd.DataFrame, class_cat: Union[int, None] = None) -> list[str]:
    if class_cat is None:
        df = df.release
    else:
        df = df.loc[df.target_category == class_cat, 'release']

    texts_raw = ' '.join(df.to_list())
    texts = preprocessing_release(texts_raw)
    return texts


def get_freq(texts: list[str]) -> dict[str, float]:
    cnt_words = Counter(texts)
    num_words = sum(cnt_words.values())
    cnt_words = {k: v / num_words for k, v in cnt_words.items()}
    cnt_words = dict(sorted(cnt_words.items(), key=lambda w: -w[1]))
    return cnt_words


def plot_wordcloud_all(data: dict, title: str):
    wordcloud = WordCloud(
        width=1200,
        height=1200,
        random_state=42,
        background_color='black',
        max_words=50,
        contour_width=2,
        contour_color='black'
        ).generate_from_frequencies(data)

    plt.figure(figsize=(10, 10))
    plt.grid(visible=False)
    plt.axis('off')
    plt.suptitle(
        title,
        fontsize=16,
        fontweight='bold'
    )
    plt.imshow(wordcloud)


def plot_all_words(data: pd.Series, title: str, ylabel: str, top=15, figsize=(18, 10)) -> None:
    plt.figure(figsize=figsize)
    sns.barplot(data=data[:top], orient='h', color='#5975A4')
    plt.suptitle(title, fontsize=16, fontweight="bold")
    plt.xlabel('Относительная частота', fontsize=12)
    plt.ylabel(ylabel)
    plt.show()


def build_vocab(corpus: list[str]) -> dict[str, str]:
    m = Mystem()
    rg = re.compile('[,=]')

    struct = m.analyze(' '.join(corpus))

    data = filter(lambda item: 'analysis' in item, struct)
    data = map(lambda item: item['analysis'], data)
    data = filter(lambda item: len(item) != 0, data)
    data = map(lambda item: item[0], data)
    data = map(lambda item: (item['lex'], PARTS_OF_SPEECH[rg.split(item['gr'])[0]]), data)

    return dict(data)


def calc_common_words(*cnt_words_dic: dict, top: int = 15) -> set[str]:
    result = set(list(cnt_words_dic[0].keys())[:top])

    for dic in cnt_words_dic[1:]:
        result.intersection_update(set(list(dic.keys())[:top]))

    return result


def plot_wordcloud_per_class(data: dict[int, dict], title: str):
    clouds = []
    targets = [-1, 0, 1]
    for target in targets:
        wordcloud = WordCloud(
                width=1200,
                height=1200,
                random_state=42,
                background_color='black',
                max_words=50,
                contour_width=2,
                contour_color='black'
            ).generate_from_frequencies(data[target])

        clouds.append(wordcloud)

    fig, axes = plt.subplots(1, 3, figsize=(28, 10))

    titles = ['Ставка снизится', 'Ставка не изменится', 'Ставка повысится']
    for ax, cloud, ttl in zip(axes, clouds, titles):
        ax.grid(visible=False)
        ax.axis('off')
        ax.set_title(ttl)
        ax.imshow(cloud)
    plt.suptitle(
            title,
            fontsize=16,
            fontweight='bold'
        )


def plot_words_per_class(data: dict[int, dict], title: str, ylabel: str, common_words: set[str], top=15) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(16, 9), layout="constrained")
    fig.suptitle(
        title,
        fontsize=16,
        fontweight='bold'
        )

    for i, (k, v) in enumerate(data.items()):
        words = pd.Series(v)[:top].reset_index()
        words.columns = ('word', 'freq')
        words['color'] = words['word'].apply(
            lambda w: 'grey' if w in common_words else COLORS[k]
        )
        words.set_index('word', inplace=True)
        sns.barplot(
            data=words,
            ax=axes[i],
            orient='h',
            y='word',
            x='freq',
            hue='word',
            legend=False,
            palette=words['color'].to_dict()
        )
        axes[i].set_ylabel(ylabel)
        axes[i].set_xlabel('Относительная частота')
    axes[0].set_title('Ставка снизится')
    axes[1].set_title('Ставка не изменится')
    axes[2].set_title('Ставка повысится')

    plt.show()


def count_char_frequency(data: pd.Series):
    counter = Counter()
    for release in data:
        counter.update(release)
    char_frequency = pd.Series(counter).sort_values(ascending=False)
    return char_frequency / char_frequency.sum()


def plot_linspace(X, title: str, df):
    pos_index = df[df.target_category == 1].index
    neg_index = df[df.target_category == -1].index
    zero_index = df[df.target_category == 0].index

    fig = go.Figure()
    fig.add_scatter(
        x=X[pos_index, 0],
        y=X[pos_index, 1],
        mode='markers',
        text=df.date.loc[pos_index],
        name='Повысить',
        marker=dict(size=10, color=COLORS[1]),
        )
    fig.add_scatter(
        x=X[neg_index, 0],
        y=X[neg_index, 1],
        mode='markers',
        text=df.date.loc[neg_index],
        name='Понизить',
        marker=dict(size=10, color=COLORS[-1]),
        )
    fig.add_scatter(
        x=X[zero_index, 0],
        y=X[zero_index, 1],
        mode='markers',
        text=df.date.loc[zero_index],
        name='Сохранить',
        marker=dict(size=10, color=COLORS[0]),
        )
    fig.update_layout(
        showlegend=True,
        height=650,
        width=650,
        margin=dict(l=20, r=20, b=10, t=40),
        title=title,
        title_font=dict(size=18, color='black', weight='bold'),
        title_x=0.5,
        )
    pyo.iplot(fig)
