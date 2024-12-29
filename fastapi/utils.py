import os
from csv import DictReader, DictWriter
import logging
import json
import re
import pickle
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score, roc_auc_score, confusion_matrix, classification_report
import pandas as pd
from nltk.corpus import stopwords
from pydantic import ValidationError
from pymystem3 import Mystem
from models import Datum
from settings import settings


def load_data_from_file(filename = f"{settings.data_path}/data.csv") -> list[dict]:
    """
    Загрузка данных из файла
    """
    result = []
    
    if os.path.isfile(filename):
        with open(filename, "r", encoding="UTF-8") as f:
            reader = DictReader(f)
            try:
                result = [Datum.model_validate(row).model_dump() for row in reader]
                logging.info("Загружены данные (%d)", len(result))
            except ValidationError as err:
                result = []
                logging.error("Ошибка валидации при чтении файла: %s", err)
    else:
        logging.warning("Файл %s отсутствует. Данные не загружены.", filename)
    return result


def save_data_to_file(save_data: list[dict]):
    """
    Сохранение данных в файл
    """
    if len(save_data) > 0:
        keys = save_data[0].keys()
        filename = f"{settings.data_path}/data.csv"
        with open(filename, "w", newline="", encoding="UTF-8") as f:
            writer = DictWriter(f, keys)
            writer.writeheader()
            writer.writerows(save_data)
            logging.info("Данные сохранены (%d)", len(save_data))


def load_models_from_file() -> dict:
    """
    Загрузка моделей из файлов
    """
    result = {}
    json_filename = f"{settings.models_path}/models.json"
    if os.path.isfile(json_filename):
        with open(json_filename, "r", encoding="UTF-8") as f:
            tmp = json.load(f)
        for key, value in tmp.items():
            try:
                pkl_filename = f"{settings.models_path}/{key}.pkl"
                with open(pkl_filename, "rb") as f:
                    pipeline = pickle.load(f)
                result[key] = value
                result[key]["pipeline"] = pipeline
                logging.info("Модель %s загружена", key)
            except OSError as e:
                logging.warning("Невозможно открыть файл %s, модель не загружена (%s)", pkl_filename, e)
    else:
        result = {}
    return result


def save_models_to_file(models: dict):
    """
    Сохранение обученных моделей
    """
    for key, value in models.items():
        try:
            pkl_filename = f"{settings.models_path}/{key}.pkl"
            with open(pkl_filename, "wb") as f:
                pickle.dump(value["pipeline"], f)
            logging.info("Модель %s сохранена", key)
        except OSError as e:
            logging.warning("Невозможно сохранить модель %s (%s)", key, e)
        value.pop("pipeline", None)
    json_filename = f"{settings.models_path}/models.json"
    with open(json_filename, "w", encoding="UTF-8") as f:
        json.dump(models, f)


def preprocessor(text):
    """
    Препроцессор для векторизации
    """
    mystem = Mystem()
    stop_words = set(stopwords.words("russian"))
    text = text.lower()
    regex = re.compile("[^а-я А-ЯЁё]")
    text = regex.sub(" ", text)
    text = " ".join(mystem.lemmatize(text))
    text = " ".join([word for word in text.split() if word not in stop_words])
    return text


def prepare_data(data_dict):
    """
    Подготовка данных для обучения и прогноза
    """
    df = pd.DataFrame(data_dict)
    df["rate"] = df.rate.shift(1)
    df.loc[0, "rate"] = 5.5
    df.set_index("date", inplace=True)
    df.drop("link", axis=1, inplace=True)
    df.sort_values("date", inplace=True)
    cur_pr = df.tail(1)
    df = df[:-1]
    X = df.drop(["target_categorial", "target_absolute", "target_relative"], axis=1)
    y = df["target_categorial"].values
    return X, y, cur_pr


def train_model(model, X, y):
    model.fit(X, y)
    return model


def calc_metrics_utils(model, X, y, window):
    """
    Функция для тестирования наших моделей. 
    Зададим начальный порог и будем обучать, 
    модель на наблюдениях до порога, 
    а тестировать на одном наблюдении после. 
    Двигая порог протестируем нашу модель. 
    И потом сравним с истинными ответами.
    """
    y_preds = []
    y_trues = []
    y_preds_proba = []
    for threshold in range(window, X.shape[0]):
        X_train = X[:threshold]
        X_test = X[threshold:]
        y_train = y[:threshold]
        y_test = y[threshold:]
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test[0].reshape(1, -1))
        y_pred_proba = model.predict_proba(X_test[0].reshape(1, -1))
        y_preds.append(y_pred.item())
        y_trues.append(y_test[0])
        y_preds_proba.append(y_pred_proba[0])
    return y_preds, y_preds_proba, y_trues
