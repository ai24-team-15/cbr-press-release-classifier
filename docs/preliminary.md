---
marp: true
---

<style scoped>
    section {
      padding-top: 0px;
      
    }
    h4 {
      font-size: 24px;
    }
    tr, td {
        background: none !important;
        border: none !important;
        width: 40%;
    }
    
    table {
        display: table;
        width: 100%;
        font-size: 18pt;
    }
    
    .icon {
        display: flex;
        gap: 0.5rem;
        margin-top: 2rem;
        font-size: 0.75rem;
    }

    .hero {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 3rem;
    }
    .left-column {
      width: 28%;
      text-align: left;
    }
    .center-column {
      width: 28%;

      display: flex;
      justify-content: center;
      align-items: center;
    }
    .right-column {
      width: 29%;
      text-align: left;
    }

    .github-link {
      display: flex;
      align-items: center;
      justify-content: center;
      margin-top: 2rem;
    }
    .center-title {
      text-align: center;
      margin-bottom: 2rem;
    }
    .hero td {
      font-size: 20pt;
    }
    </style>

<div class="center-title">

# Команда 15

## Классификатор пресс-релизов ЦБ с предсказанием будущей ключевой ставки

</div>

<div class="hero">

<div class="left-column">
  <table>
    <tr><h4>Куратор проекта:</h4></tr>
      <tr><td>Ковалева Александра</td></tr>
  </table>
</div>

<div class="center-column">
  <img src="./img/title.jpg" class="center-image" alt="Логотип проекта">
</div>

<div class="right-column">
  <table>
    <tr><h4>Участники проекта:</h4></tr>
    <tr>
      <td>Жарковский Дмитрий</td> 
    </tr>
    <tr> 
      <td>Кузьмин Дмитрий</td>
    </tr>
    <tr>
      <td>Куимов Владислав</td> 
    </tr>
      <td>Хадиев Руслан</td>
    </tr>
  </table>
</div>

</div>

<div class="github-link">
  <img src="https://github.githubassets.com/favicons/favicon.svg" width="24"/>
  <a href="https://github.com/ai24-team-15">https://github.com/ai24-team-15</a>
</div>

---
<style scoped>
  section {
    padding-top: 25px;
  }
  h1 {
    text-align: center;
  }
  h4 {
    font-size: 28px;
  }
  .task-container {
    display: flex;
    flex-direction: column;
    gap: 0rem;
  }
  .context-box {
    background-color: #f5f5f5;
    border-left: 6px solid #4285f4;
    padding: 0.5rem;
    margin: 0 0;
    font-size: 28px;
  }
  .core-box {
    background-color: #f5f5f5;
    border-left: 6px solid #aa0000;
    padding: 0.5rem;
    margin: 0 0;
    font-size: 28px;
  }
  .solution-box {
    background-color: #f5f5f5;
    border-left: 6px solid #00aa00;
    padding: 0.5rem;
    margin: 0 0;
    font-size: 28px;
  }
</style>

<h1>Постановка задачи</h1>

<div class="task-container">

  <h4>Контекст задачи:</h4>
  <div class="context-box">
    После каждого заседания совета директоров по ключевой ставке Центральный Банк публикует пресс-релизы
  </div>

  <h4>Суть проблемы:</h4>
  <div class='core-box'>
    Текст пресс-релиза содержит косвенные сигналы о будущих решениях ЦБ, которые необходимо выявить, формализовать и автоматизировать
  </div>

  <h4>Решение:</h4>
  <div class='solution-box'>
    Создать классификатор текстов, прогнозирующий решение о ключевой ставке на основе семантического анализа
  </div>
</div>

---

<style scoped>
  section {
    padding-top: 25px;
    font-size: 28px;
  }
  h1 {
    padding-top: 0px;
    margin-top: 0px;
    text-align: center
  }
  .description-box {
    padding-bottom: 100px;
  }
</style>

<h1>Описание данных</h1>
<div class='description-box'>
<h4>Собранный датасет имеет следующие признаки:</h4>

- `date` - дата опубликования пресс-релиза;
- `link` - ссылка на пресс-релиз;
- `title` - заголовок пресс-релиза;
- `release` - текст пресс-релиза;
- `rate` - ключевая ставка утвержденная во время следующего заседания;
- `inflation` - значение инфляции в месяц следующего заседания (годовая);
- `usd` - курс доллара на день следующего заседания;
</div>

---
<style scoped>
  section {
    padding-top: 25px;
    justify-content: flex-start;

  }
  h1 {
    padding-top: 0px;
    margin-top: 0px;
    text-align: center
  }
  .data-container {
    display: flex;
    flex-direction: column;
    gap: 0rem;
  }
  .dataset-box {
    background-color: #f5f5f5;
    border-left: 6px solid #aa0000;
    padding: 0.5rem;
    margin: 0 0;
    font-size: 24px;
  }
  .corr-box {
    background-color: #f5f5f5;
    border-left: 6px solid #00aa00;
    padding: 0.5rem;
    margin: 0 0;
    font-size: 24px;
  }
  .balance-box {
    background-color: #f5f5f5;
    border-left: 6px solid #e5e433;
    padding: 0.5rem;
    margin: 0 0;
    font-size: 24px;
  }
</style>

<h1>Особенности данных</h1>
<h4>Мало данных:</h4>
<div class='dataset-box'>
  Датасет менее 100 наблюдений. Имеет место проблема переобучения.
</div>
<h4>Корреляция:</h4>
<div class='corr-box'>
  Наблюдается корреляция между ключевой ставкой, инфляцией и курсом доллара.
</div>
<h4>Дисбаланс классов:</h4>
<div class='balance-box'>
Наблюдается небольшой дисбаланс по классам:
<ul>
    <li> 43,2% наблюдений - сохранение ставки</li>
    <li>31,6% - понижение ставки</li>
    <li>25,3% - повышение ставки</li>
</ul>
</div>

---

<h1>Исследовательский анализ</h1>

---

<style scoped>
  section {
    padding-top: 25px;
    justify-content: flex-start;

  }
  h1 {
    padding-top: 0px;
    margin-top: 0px;
    text-align: center
  }
  p {
    font-size: 24px;
  }

  .description-box {
    background-color: #f5f5f5;
    border-left: 6px solid #aa0000;
    padding: 0.5rem;
    margin: 0 0;
    font-size: 24px;
  }
</style>

<h1>Динамика ключевой ставки</h1>

  <img src='./img/dinamic_rate.png'/>
  <p>
  💡 Ставку повышают при высокой инфляции<br>
  💡 Мы видим три цикла роста ставки, сейчас мы находимся на пике третьего цикла<br>
  💡 С долларом корреляция значительно слабее, в период с 2018 года по 2021 ставка снижается, а доллар растет
</p>

---

<style scoped>
  section {
    padding-top: 25px;
    justify-content: flex-start;

  }
  h1 {
    padding-top: 0px;
    margin-top: 0px;
    text-align: center
  }
  p {
    font-size: 24px;
  }
  .description-box {
    background-color: #f5f5f5;
    border-left: 6px solid #aa0000;
    padding: 0.5rem;
    margin: 0 0;
    font-size: 24px;
  }
</style>

<h1>Длина пресс-релизов</h1>

![](img/length.png)

<p>💡 За длинными пресс-релизами как правило следует повышение ключевой ставки. Возможно, руководство банка пытается оправдать свое решение.
</p>

---

<style scoped>
    section {
    padding-top: 25px;
    justify-content: flex-start;

  }
  h1 {
    padding-top: 0px;
    margin-top: 0px;
    text-align: center
  }
  .two-columns {
      display: flex;
      justify-content: space-between;
      /* align-items: center; */
      /* gap: 2rem; */
      /* margin-top: 1rem; */
  }
  .image-column {
      width: 65%;

  }
  .text-column {
      flex: 1;
      text-align: center;
      width: 45%;
      align-items: center;
      margin-top: 150px;
  }
  img {
      width: 95%;
      height: 575px;
  }
</style>

<h1>Визуализация на плоскости</h1>

<div class="two-columns">
    <div class="image-column">
        <img src="img/tsne.png" />
    </div>
    <div class="text-column">
      💡 T-SNE визуализация разбила тексты пресс-релизов на 2 кластера. Возможно в 2018 году сменился редактор и тексты сильно поменялись.
    </div>
</div>

---

<style scoped>
    section {
    padding-top: 25px;
    justify-content: flex-start;

  }
  h1 {
    padding-top: 0px;
    margin-top: 0px;
    text-align: center
  }
</style>


<h1>Частота слов</h1>

<center>
    <img src="img/wordcloud.png" />
</center>

<p>
  💡 Частота слов не сильно меняется от класса к классу, но все же слово инфляция реже встречается перед снижением ставки<br>
  💡 Частотность слов в пресс-релизах очень сильно отличается от стандартной частотности русского языка
</p>

---
<style scoped>
    section {
    padding-top: 25px;
    justify-content: flex-start;

  }
  h1 {
    padding-top: 0px;
    margin-top: 0px;
    text-align: center
  }
  div {
    height: 1000px
  }
</style>
<div>
<h1>Метрика качества</h1>

<h4>Метрикой качества выбрана <b>ROC AUC OvO</b></h4>

<p>
  ✅  Она является интегральной (не зависит от порога перевода вероятностей в классы)
</p> 
 ✅ Не чувствительна к дисбалансу классов (в нашем датасете наблюдается небольшой дисбаланс).
</div>

---

<h1>Классический Machine Learning</h1>

---

<style scoped>
    section {
        padding-top: 25px !important;
        margin: 0 !important;
    }
    h1 {
        padding-top: 0px !important;
        margin: 0 !important;
        text-align: center;

        top: 0;
        width: 100%;
    }
    .approach-slide {
        display: flex;
        flex-direction: column;
        height: 100vh;
        padding-top: 0px; /* Отступ для заголовка */
        background: linear-gradient(to bottom, #f8f9fa, #e9ecef);
    }
    .approach-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 30px;
        margin-top: 20px;
        height: calc(100% - 40px);
    }
    .approach-card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .approach-card:hover {
        transform: translateY(-5px);
    }
    .approach-title {
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 10px;
        font-size: 24px;
        margin-bottom: 15px;
    }
    .approach-list {
        list-style-type: none;
        padding-left: 0;
    }
    .approach-list li {
        background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="%233498db" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle></svg>') no-repeat left center;
        padding-left: 25px;
        margin-bottom: 10px;
        line-height: 1.5;
    }
</style>

<h1>Используемые подходы</h1>

<div class="approach-slide">
    <div class="approach-container">
        <div class="approach-card">
            <h3 class="approach-title">Векторизация текстов</h3>
            <ul class="approach-list">
                <li>Bag-of-Words (BoW)</li>
                <li>Tf-Idf</li>
                <li>N-граммы</li>
                <li>Word2Vec</li>
                <li>GloVe</li>
            </ul>
        </div>

  <div class="approach-card">
            <h3 class="approach-title">Классификаторы</h3>
            <ul class="approach-list">
                <li>Логистическая регрессия</li>
                <li>SVM</li>
                <li>Naive Bayes</li>
                <li>KNN</li>
                <li>Random Forest</li>
                <li>Бустинговые методы</li>
            </ul>
        </div>

  <div class="approach-card">
            <h3 class="approach-title">Отбор признаков</h3>
            <ul class="approach-list">
                <li>From model</li>
                <li>PCA</li>
            </ul>
        </div>
    </div>
</div>

---

<style scoped>
    section {
        padding: 1rem !important;
    }
    
    table {
        display: table;
        width: 100%;
    }
    
    table * {
        font-size: 10pt;
    }
    
    .yellow {
        background-color: yellow;
    }
</style>

# Метрики качества моделей

<table border="1" class="dataframe">
  <thead>
    <tr>
      <th>Модель</th>
      <th>Гиперпараметры</th>
      <th>ROC AUC OvO</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Минимальный бейзлайн</th>
      <td>-</td>
      <td>0.749583</td>
    </tr>
    <tr>
      <th>BoW (тексты релизов) + LogReg с L1-регуляризацией</th>
      <td>C=7.241655172413794, penalty='l1', solver='liblinear'</td>
      <td>0.770722</td>
    </tr>
    <tr>
      <th>BoW + LogReg с L1-, L2-регуляризацией</th>
      <td rowspan="3">C=10, l1_ratio=0.1, max_iter=10000, penalty='elasticnet', solver='saga'</td>
      <td>0.873204</td>
    </tr>
    <tr>
      <th>BoW (тексты релизов + заголовки) + LogReg</th>
      <td>0.871488</td>
    </tr>
    <tr>
      <th>BoW (тексты релизов + числовые переменные) + LogReg</th>
      <td>0.863797</td>
    </tr>
    <tr>
      <th>BoW (тексты релизов) + SVM</th>
      <td>C=7, kernel='linear', probability=True</td>
      <td>0.837417</td>
    </tr>
    <tr>
      <th>TF-IDF (тексты релизов) + LogReg с L1-регуляризацией</th>
      <td>C=10.0, penalty='l1', solver='liblinear'</td>
      <td>0.787614</td>
    </tr>
    <tr>
      <th>TF-IDF (тексты релизов c доп. фильтрацией) + LogReg</th>
      <td rowspan="3">C=10, l1_ratio=0.1, max_iter=10000, penalty='elasticnet', solver='saga'</td>
      <td>0.903270</td>
    </tr>
    <tr>
      <th>TF-IDF (тексты релизов + заголовки) + LogReg</th>
      <td>0.881341</td>
    </tr>
    <tr>
      <th>TF-IDF (тексты релизов + числовые переменные) + LogReg</th>
      <td>0.837195</td>
    </tr>
    <tr class="yellow">
      <th>TF-IDF (тексты релизов) + SVM</th>
      <td>C=10, kernel='linear', probability=True</td>
      <td>0.927695</td>
    </tr>
    <tr>
      <th>N-граммы плюс Naive Bayes</th>
      <td>ngram_range(3, 6)</td>
      <td>0.777142</td>
    </tr>
    <tr>
      <th>Word2Vec + LogReg</th>
      <td>C=1, l1_ratio=0.9, max_iter=10000, penalty='elasticnet', solver='saga'</td>
      <td>0.732520</td>
    </tr>
    <tr>
      <th>Word2Vec (предобученная модель) + LogReg</th>
      <td>C=0.1, l1_ratio=0.1, max_iter=10000, penalty='elasticnet', solver='saga'</td>
      <td>0.765176</td>
    </tr>
    <tr>
      <th>Word2Vec (предобученная модель с фильтрацией) + LogReg</th>
      <td>C=10, l1_ratio=0.5, max_iter=10000, penalty='elasticnet', solver='saga'</td>
      <td>0.697273</td>
    </tr>
    <tr>
      <th>Word2Vec (предобученная модель) + SVM</th>
      <td>C=7, kernel='linear', probability=True</td>
      <td>0.749317</td>
    </tr>
    <tr>
      <th>GloVe + SVM</th>
      <td>C=3, probability=True</td>
      <td>0.768338</td>
    </tr>
  </tbody>
</table>

---

# Сервис FastAPI

Реализован сервис на FastAPI для управления моделями и данными.

**Данные:** Загрузка данных с помощью post-запроса или с S3 сервера. При остановке сервиса данные сохраняются и загружаются при последующем запуске.

**Обучение моделей:** Обучение производится с заданными в запросе гиперпараметрами, в отдельном процессе. Реализованы две модели, показавшие лучшие результаты на предыдущем чекпоинте.

**Инференс моделей:** Реализован как обычный прогноз, так и вычисление метрик при обучении на части данных.

**Управление моделями:** Как и данные, модели сохраняются во время остановки сервиса и загружаются при запуске.

---

# Приложение Streamlit

Реализован многостраничный пользовательский-интерфейс для взаимодействия с сервисом.

**Загрузка данных:** Загрузка своих данных, либо выбрать актуальные данные.

**Исследовательский анализ:** Баланс классов, динамика ставки, курса доллара США и годовой инфляции, длина текстов, облака слов, t-SNE визуализация.

**Машинное обучение:** Обучение моделей с выбором гиперпараметров, сравнение моделей между собой и предсказание с помощью выбранной модели.

---

# Инфраструктура

- Docker-образы сервиса и веб-приложения.
- Конфигурация Docker Compose для запуска приложения.
- Система сбора логов ELK.
- Деплой в Yandex Cloud с использованием сервисов:
    - Object Storage
    - Container Registry
    - Compute Cloud
    
Приложение доступно по адресу http://cbr-classifier.ddns.net/

---

<style scoped>
    section {
        padding: 1rem !important;
    }
    
    img {
        width: 80%;
        height: auto;
    }
    
    p:has(> img) {
        text-align: center;
    }
</style>

#### Демонстрация работы сервиса

![screencast](img/app_screencast.gif)

---

<style scoped>
    section {
        padding: 1rem !important;
    }
    
    img {
        width: 80%;
        height: auto;
    }
    
    p:has(> img) {
        text-align: center;
    }
</style>

#### Демонстрация системы сбора логов

![screencast](img/logs_screencast.gif)

---

# Распределение работы в команде

- **Куимов Владислав**: часть скрапера, немного EDA (t-SNE), некоторые модели (c GloVe), инфраструктура (Docker, ELK, деплой в Yandex Cloud)
- **Жарковский Дмитрий**: часть скрапера, часть исследователького анализа, модели с Bow, Tf-Idf и Word2Vec, Streamlit в последнем чекпоинте.
- **Кузьмин Дмитрий**: часть скрапера, сервис FastAPI.
- **Хадиев Руслан**: участие в обсуждениях по возможным путям реализации проекта. Подготовка выводов по моделям и результатам реализации проекта. 

---

# Цели по проекту на второе полугодие

- Подготовка дополнительных эмбеддингов текстовых наблюдений (Word2Vec, FastText и т.п.).
- Проектирование и обучение нейросетевых моделей, используя полученные ранее эмбединги и табличные данные.
- Дообучение языковых моделей (например, BERT) на наших данных.

#### Дополнительно:

- Ансамблирование моделей.
- Предсказание, на сколько процентных пунктов изменится ставка.
- Аугментация данных.

---

# Итоги

- Собран исходный датасет и проведен подробный исследовательский анализ.
- Подобрана модель, показавшую достаточно высокое качество по выбранной метрике.
- Разработаны и развернуты сервис и веб-приложение, позволяющие исследовать исходный датасет, обучать, применять и сравнивать модели.
