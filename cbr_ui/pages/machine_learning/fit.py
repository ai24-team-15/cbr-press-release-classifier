import asyncio
import streamlit as st
from tools.api import client
from tools.config import log as logger


# Заголовок страницы
st.header("Обучение модели")

# Инициализация пустого словаря для передачи данных в запрос
payload = {}

# Выбор типа модели
payload["type"] = st.radio("Выберите модель", ["LogisticRegression", "SVC"])

st.subheader("Выберите гиперпараметры модели")

# Словарь для хранения значений гиперпараметров
params = {}

# Выбор значения гиперпараметра C с помощью слайдера
params["C"] = st.slider("C", 0.0, 10.0, step=0.001, value=1.0, format="%.3f")

# Выбор значения гиперпараметра tol с помощью слайдера
params["tol"] = st.slider("tol", 1e-6, 1e-3, step=0.000001, format="%.6f", value=1e-4)

# Условия для настройки гиперпараметров для LogisticRegression
if payload["type"] == "LogisticRegression":

    # Выбор типа регуляризации (penalty)
    params["penalty"] = st.radio("penalty", ["l2", None, "l1", "elasticnet"])

    # Условия для выбора solver в зависимости от выбранной регуляризации
    if params["penalty"] == "l2":
        params["solver"] = st.radio(
            "solver",
            [
                "lbfgs",
                "liblinear",
                "newton-cg",
                "newton-cholesky",
                "sag",
                "saga"
            ])
    if params["penalty"] is None:
        params["solver"] = st.radio(
            "solver",
            [
                "lbfgs",
                "newton-cg",
                "newton-cholesky",
                "sag",
                "saga"
            ])
    if params["penalty"] == "l1":
        params["solver"] = st.radio(
            "solver",
            [
                "liblinear",
                "saga"
            ])
    if params["penalty"] == "elasticnet":
        params["solver"] = "saga"

    # Дополнительная настройка для solver 'liblinear', добавление гиперпараметра dual
    if params["penalty"] == "l2" and params["solver"] == "liblinear":
        params["dual"] = st.radio("dual", [False, True])

    # Выбор максимального числа итераций для оптимизации
    params["max_iter"] = st.slider("max_iter", 100, 1000, step=1, value=100)

    # Добавление гиперпараметра warm_start для solver 'liblinear'
    if params["solver"] == "liblinear":
        params["warm_start"] = st.radio("warm_start", [False, True])

    # Если используется penalty 'elasticnet', добавляется гиперпараметр l1_ratio
    if params["penalty"] == "elasticnet":
        params["l1_ratio"] = st.slider("l1_ratio", 0.0, 1.0, step=0.01, value=0.5)
else:
    # Условия для настройки гиперпараметров для SVC
    # Выбор типа ядра (kernel)
    params["kernel"] = st.radio("kernel", ["rbf", "linear", "poly", "sigmoid"])

    # Если выбрано ядро 'poly', добавляем гиперпараметр degree
    if params["kernel"] == "poly":
        params["degree"] = st.slider("degree", 1, 5, step=1, value=3)

    # Если ядро не линейное, добавляем гиперпараметр gamma
    if params["kernel"] != "linear":
        params["gamma"] = st.radio("gamma", ["scale", "auto"])

    # Для некоторых типов ядер добавляется параметр coef0
    if params["kernel"] in set(["poly", "sigmoid"]):
        params["coef0"] = st.slider("coef0", -1.0, 1.0, step=0.01, value=0.0)

    # Установка параметра shrinking
    params["shrinking"] = st.radio("shrinking", [False, True])

    # Включаем вероятность для всех типов ядра
    params["probability"] = True

# Добавление выбранных гиперпараметров в payload
payload["hyperparameters"] = params

# Ввод ID модели
payload["model_id"] = st.text_input("Введите id модели")

# Ввод описания модели
payload["description"] = st.text_input("Введите описание модели")

# Обработка нажатия кнопки "Обучить модель"
if st.button("Обучить модель"):
    # Проверка на наличие ID модели
    if not payload["model_id"]:
        st.error("Введите id модели")  # Если ID не введен, выводится ошибка
    else:
        try:
            # Вызов асинхронного метода fit API с передачей данных
            response = asyncio.run(
                client.fit('/fit', payload)
            )
        except Exception as e:
            logger.error("Ошибка при обучении модели: %s", e)
            raise e

        logger.info("Модель %s успешно обучена.", payload["model_id"])

        # Вывод статуса ответа от API
        st.warning(response["status"])
