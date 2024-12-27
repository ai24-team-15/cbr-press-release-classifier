import streamlit as st
import logging
import pandas as pd

from tools.utils import COLORS, CATEGORIAL_NAMES
from tools.plots import plot_len_text, plot_boxplot
from tools.config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

st.subheader('Распределение длин текстов релизов')

logger.info("Начало построения графиков длин текстов.")
if 'data' in st.session_state:
    data = st.session_state['data']
else:
    data = pd.read_csv('./data/cbr-press-releases.csv')
    st.session_state['data'] = data
    st.session_state['other_data'] = False

if 'target_categorial_name' not in data.columns:
    data['target_categorial_name'] = data.target_categorial.map(CATEGORIAL_NAMES)

st.plotly_chart(plot_len_text(data))

# Печать статистики
st.write(f'Средняя длина текстов - {data["release"].str.len().mean():.2f} символов')
st.write(f'Самый длинный текст - {data["release"].str.len().max()} символов')
st.write(f'Самый короткий текст - {data["release"].str.len().min()} символов')

data['release_len'] = data.release.str.len()

st.subheader('Распределение длин текстов релизов с разделением по классам')
st.plotly_chart(plot_boxplot(data, COLORS))
logger.info("Графики длин текстов построены.")

big_text = """
Анализ длины текстов для прогнозирования событий представляет собой один из инструментов обработки данных. Особенно, данный инструмент отлично подходит для анализа новостных лент и других текстовых источников вроде пресс-релизов ЦБ.  
При анализе текста в пресс-релизах ЦБ наблюдается следующая картина:  
- Пресс релизы ЦБ относящиеся к увеличению ключевой ставки имеют более длинные тексты чем для других наблюдений. Данный результат, по нашему мнению, связан с необходимостью аргументировать более подробно причины увеличения ставки, так как увеличение ставки оказывает негативное влияние как на физических, так и на юридических лиц (увеличиваются их расходы на обслуживание кредитов, на возможность взять кредиты, а это в свою очередь влияет на производственные процессы и на потребление в целом в экономике);  
- При снижении ключевой ставки ЦБ длинна текста самая короткая. Скорее всего это обусловлено отсутствием необходимости подробно объяснять причины снижения ставки, так как снижение ставки связано с позитивными макроэкономическими данными в экономике и будет восприниматься позитивно;  
- зависимость ключевой ставки от длины текста подтверждается корреляцией – 0,25.  

"""
st.write(big_text)
