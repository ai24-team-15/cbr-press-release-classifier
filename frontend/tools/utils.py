import re
from typing import Union, List, Dict, Set
from collections import Counter
import os

import pandas as pd
import numpy as np
import nltk
from pymystem3 import Mystem
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE
import aiohttp

# Загрузка необходимых ресурсов NLTK
nltk.download('stopwords')

# Определение цветов для визуализации
COLORS = {
    'Снижение ставки': '#4D6D7F',
    'Сохранение ставки': '#1A4E1A',
    'Повышение ставки': '#A03B2A',
    -1: '#4D6D7F',
    1: '#1A4E1A',
    0: '#A03B2A'
}

# Определение категорий
CATEGORIAL_NAMES = {
    -1: 'Снижение ставки',
    1: 'Повышение ставки',
    0: 'Сохранение ставки'
}


@st.cache_resource
def preprocessing_release(text: str) -> List[str]:
    """
    Предобработка текста: лемматизация, удаление стоп-слов и символов, не относящихся к кириллице.

    Аргументы:
        text (str): Исходный текст.

    Возвращает:
        List[str]: Список обработанных слов.
    """
    stop_words = set(nltk.corpus.stopwords.words('russian'))
    regex = re.compile('[^а-я ]')
    mystem = Mystem()

    text = text.lower()  # Приведение текста к нижнему регистру
    text = regex.sub(' ', text)  # Удаление всех символов, кроме кириллицы и пробелов
    text = filter(lambda w: not w.isspace(), mystem.lemmatize(text))  # Лемматизация
    text = list(filter(lambda w: w not in stop_words and len(w) != 1, text))  # Удаление стоп-слов и коротких слов
    return text


@st.cache_data
def get_preprocess_texts(df: pd.DataFrame, class_cat: Union[int, None] = None) -> List[str]:
    """
    Извлекает и обрабатывает текстовые данные из DataFrame в зависимости от категории.

    Аргументы:
        df (pd.DataFrame): DataFrame с текстовыми данными.
        class_cat (Union[int, None], optional): Категория для фильтрации. По умолчанию None.

    Возвращает:
        List[str]: Список обработанных слов из выбранных текстов.
    """
    if class_cat is None:
        df = df.release
    else:
        df = df.loc[df.target_categorial == class_cat, 'release']

    texts_raw = ' '.join(df.to_list())  # Объединение текстов в одну строку
    texts = preprocessing_release(texts_raw)  # Предобработка текста
    return texts


@st.cache_data
def get_freq(texts: List[str]) -> Dict[str, float]:
    """
    Вычисляет частоту слов в списке текстов.

    Аргументы:
        texts (List[str]): Список слов.

    Возвращает:
        Dict[str, float]: Словарь с частотами слов (слово: частота).
    """
    cnt_words = Counter(texts)  # Подсчет количества каждого слова
    num_words = sum(cnt_words.values())  # Общее количество слов
    cnt_words = {k: v / num_words for k, v in cnt_words.items()}  # Нормализация частот
    cnt_words = dict(sorted(cnt_words.items(), key=lambda w: -w[1]))  # Сортировка по убыванию частоты
    return cnt_words


@st.cache_data
def calc_common_words(*cnt_words_dic: Dict[str, float], top: int = 15) -> Set[str]:
    """
    Вычисляет общие слова среди нескольких словарей с частотами.

    Аргументы:
        *cnt_words_dic (Dict[str, float]): Словари с частотами слов.
        top (int, optional): Количество верхних слов для учета. По умолчанию 15.

    Возвращает:
        Set[str]: Множество общих слов среди словарей.
    """
    result = set(list(cnt_words_dic[0].keys())[:top])  # Берем топ-слова из первого словаря
    for dic in cnt_words_dic[1:]:
        result.intersection_update(set(list(dic.keys())[:top]))  # Оставляем только общие слова

    return result


@st.cache_resource
def get_vectors(df: pd.DataFrame) -> np.ndarray:
    """
    Генерирует t-SNE векторы для корпуса текстов в DataFrame.

    Аргументы:
        df (pd.DataFrame): DataFrame с колонкой 'corpus'.

    Возвращает:
        np.ndarray: Двумерные t-SNE векторы.
    """
    vec = TfidfVectorizer(analyzer=lambda x: x)  # Инициализация векторизатора
    X = vec.fit_transform(df.corpus)  # Преобразование текстов в векторы

    tsne = TSNE(n_components=2, random_state=42)  # Инициализация t-SNE
    X_tsne = tsne.fit_transform(X.toarray())  # Преобразование в двумерное пространство

    return X_tsne


async def download_file(url: str, filename: str) -> None:
    """
    Асинхронная загрузка файла с указанного URL и сохранение его локально.

    Аргументы:
        url (str): URL для загрузки файла.
        filename (str): Имя файла для сохранения.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            os.makedirs("data", exist_ok=True)  # Создание папки, если ее нет
            with open(filename, 'wb') as f:
                while True:
                    chunk = await response.content.read(1024)  # Загрузка файла частями
                    if not chunk:
                        break
                    f.write(chunk)


def get_data_for_wordclouds(data: pd.DataFrame) -> Dict[str, Union[Dict[int, Dict[str, float]], Set[str]]]:
    """
    Обрабатывает данные для генерации частот слов и общих слов для облаков слов.

    Аргументы:
        data (pd.DataFrame): DataFrame с колонками 'target_categorial' и текстовыми данными.

    Возвращает:
        Dict[str, Union[Dict[int, Dict[str, float]], Set[str]]]:
            Словарь с частотами слов, общими словами и частотами для всех классов.
    """
    frequencies = {}
    unique_target = data.target_categorial.unique()  # Уникальные категории
    unique_target = unique_target[~np.isnan(unique_target)]  # Исключение NaN

    for target in unique_target:
        frequencies[target] = get_preprocess_texts(data, target)  # Предобработка текста для каждой категории

    texts_all_class = get_preprocess_texts(data)  # Тексты всех категорий

    for target in unique_target:
        frequencies[target] = get_freq(frequencies[target])  # Частоты слов для каждой категории

    cnt_words_all_classes = get_freq(texts_all_class)  # Частоты слов для всех категорий
    common_words = calc_common_words(*frequencies.values())  # Общие слова между категориями

    return {'data': frequencies, 'common_words': common_words, 'cnt_words_all_classes': cnt_words_all_classes}
