import streamlit as st
import pandas as pd
from tools.plots import plot_pie
from tools.utils import COLORS, CATEGORIAL_NAMES
from tools.config import log as logger


# Отображение подзаголовка в приложении Streamlit
st.subheader("Распределение решений по ключевой ставке")

# Логирование начала процесса построения графиков
logger.info("Начало построения графиков распределения по категориям.")

# Проверка наличия данных в session_state или их загрузка из файла
if "data" in st.session_state:
    # Используем данные, уже загруженные в session_state
    data: pd.DataFrame = st.session_state["data"]
else:
    # Если данные не загружены, читаем их из файла по умолчанию
    data: pd.DataFrame = pd.read_csv("./data/cbr-press-releases.csv")
    st.session_state["data"] = data
    st.session_state["other_data"] = False

# Добавление колонки с категориями, если она отсутствует
if "target_categorial_name" not in data.columns:
    data["target_categorial_name"] = data.target_categorial.map(CATEGORIAL_NAMES)

# Подготовка данных для круговой диаграммы
# Группировка данных по категориям и расчет доли каждой категории
category_counts: pd.Series = data.groupby("target_categorial_name").title.count()
df: pd.DataFrame = (category_counts / category_counts.sum()).reset_index()

# Переименование колонок для наглядности
df = df.rename(
    columns={
        "target_categorial_name": "Решение по ключевой ставке",
        "title": "Доля",
    }
)

# Построение круговой диаграммы и её отображение в Streamlit
st.plotly_chart(plot_pie(df, COLORS))
logger.info("Графики распределения по категориям успешно построены.")

# Текстовое описание круговой диаграммы
big_text = """
На графике представлено общее количество наблюдений (96) распределённых по трем категориям.
Больше всего наблюдений отнесено в категорию сохранить ключевую ставку ЦБ – 42,7 %;
На втором месте находятся наблюдения, которые приводят к снижению ключевой ставке ЦБ – 31,3%;
И на третьем месте находятся наблюдения увеличивающие ключевую ставку ЦБ – 26%.
Такое распределение на круговом графике обусловлено циклическим развитием экономики (спад, рост)
и разной продолжительностью этих трендов. Подъем ключевой ставки происходит в кризисные периоды
для охлаждения экономики и стабилизации инфляции и длятся они не так продолжительно, как периоды
роста, что и наблюдаем на круговом графике.
"""

# Отображение текстового описания в приложении Streamlit
st.write(big_text)
