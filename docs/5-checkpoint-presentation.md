---
marp: true
---

<!-- theme: default -->
<!-- paginate: true -->
<!-- lang: ru -->

<style scoped>
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
</style>

<style>
    .container {
        display: grid;
        grid-template-columns: 50% 50%;
        grid-template-rows: min-content;
    }
    
    .item-img {
        grid-column-start: 2;
        grid-row-end: span 2;
        text-align: right;
    }
    
    table {
        font-size: 16px;
        width: 50%;
        align: center;
    }

    .metrics-container {
        display: flex;
        /* grid-template-columns: 30% 70%;
        grid-template-rows: min-content; */
    }

    .metrics-img {
        /* grid-column-start: 2;
        grid-row-end: span 2;
        text-align: right; */
        flex: 70%;
    }

    .metrics-text {
        width: 30%;
        text-align: center;
        padding: 10px;
    }
    
    /* img[alt~="image"] {
        float: right;
        width: 80%;
    } */
</style>

# Команда 15

## Классификатор пресс-релизов ЦБ с предсказанием будущей ключевой ставки

**Куратор проекта**: Ковалева Александра

**Участники проекта**:

<table>
    <tr>
        <td>Жарковский Дмитрий</td>
        <td>Кузьмин Дмитрий</td>
    </tr>
    <tr>
        <td>Иванов Иван</td>
        <td>Хадиев Руслан</td>
    </tr>
    <tr>
        <td>Куимов Владислав</td>
        <td></td>
    </tr>
</table>

<p class="icon">
    <img src="https://github.githubassets.com/favicons/favicon.svg"/>
    <a href="https://github.com/ai24-team-15">https://github.com/ai24-team-15</a>
</p>

---

# Постановка задачи

ЦБ каждый раз после заседания по ключевой ставке на сайте публикует пресс-релизы, в которых рассказывается про состояние экономики, инфляцию, спрос на продукты, услуги и т.д. и объясняет причину изменения/не изменения ставки.

Задача состоит в том, чтобы по семантике текста понять, что будет происходить с ключевой ставкой после на следующем заседании: ЦБ ее поднимет, опустит или оставит неизменной. Необходимо создать классификатор, который сможет определить тексты на 3 класса: -1 (ставка опустится), 0 (останется неизменной), 1 (ставку повысят).

---

# Лучшая линейная модель

На предыдущих этапах был построен следующий пайплайн на основе линейной модели, показавший наилучший результат:
- TF-IDF векторизация текстов пресс-релизов
- Отбор признаков при помощи логистической регрессии с L1-регуляризацией
- SVM-классификатор

---

<style scoped>
    table, td, th {
        width: 100%;
    }
</style>

# Лучшая линейная модель: метрики качества

<div class="container">
<div>

| Метрика     | Значение |
|-------------|----------|
| Accuracy    | 0.691176 |
| F1-score    | 0.693718 |
| Recall      | 0.700864 |
| Precision   | 0.691017 |
| ROC-AUC OvR | 0.840529 |
| ROC-AUC OvO | 0.844115 |

</div>
<div class="item-img">
    <img alt="img" src="svc_cm.png"/>
</div>
<div>
Метод опорных векторов показал достаточно хорошее качество, едва удалось побить эти метрики с помощью нелинейных моделей.
</div>
</div>

---

# Нелинейные модели: KNN

Лучший пайплайн на основе классификатора KNN включает в себя:
- TF-IDF векторизация текстов пресс-релизов
- Отбор признаков при помощи логистической регрессии с L1-регуляризацией
- KNN-классификатор

---

<style scoped>
    table, td, th {
        width: 100%;
    }
</style>

# KNN: метрики качества

<div class="container">
<div>

| Метрика     | Значение |
|-------------|----------|
| Accuracy    | 0.779412 |
| F1-score    | 0.779213 |
| Recall      | 0.780731 | 
| Precision   | 0.779259 |
| ROC-AUC OvR | 0.834168 |
| ROC-AUC OvO | 0.835548 |

</div>
<div class="item-img">
    <img alt="img" src="knn_cm.png"/>
</div>
<div>
По метрикам ROC-AUC качество несколько уменьшилось относительно линейной модели, но по другим метрикам результат улучшился.
</div>
</div>

---

# Нелинейные модели: TimeSeries (KNN)

Модель использующая подходы временных рядов, тексты пресс-релизов в данной модели не используются.

Пайплайн этой модели включает в себя:
- Генерацию 4 лаговых признаков целевой переменной
- Герерацию 3 лаговых признаков, курса доллара, инфляции и величины процентной ставки
- Генерацию относительного прироста для каждого признака из предыдущего пункта
- Масштабирование признаков
- KNN-классификатор

---

<style scoped>
    table, td, th {
        width: 100%;
    }
</style>

# TimeSeries: метрики качества

<div class="container">
<div>

| Метрика     | Значение |
|-------------|----------|
| Accuracy    | 0.705882 |
| F1-score    | 0.713066 |
| Recall      | 0.709940 | 
| Precision   | 0.717836 |
| ROC-AUC OvR | 0.806009 |
| ROC-AUC OvO | 0.809599 |

</div>
<div class="item-img">
    <img alt="img" src="timeseries_cm.png"/>
</div>
<div>
Модель одинаково хорошо детектирует все виды классов, и не разу не перепутала повышение ставки с понижением.
</div>
</div>

---

# Нелинейные модели: RandomForest

Пайплайн для модели RandomForest включает в себя:
- TF-IDF векторизация текстов пресс-релизов
- Отбор признаков при помощи PCA
- RandomForest-классификатор

---

<style scoped>
    table, td, th {
        width: 100%;
    }
</style>

# RandomForest: метрики качества

<div class="container">
<div>

| Метрика     | Значение |
|-------------|----------|
| Accuracy    | 0.632353 |
| F1-score    | 0.631884 |
| Recall      | 0.620548 | 
| Precision   | 0.681082 |
| ROC-AUC OvR | 0.817684 |
| ROC-AUC OvO | 0.822178 |

</div>
<div class="item-img">
    <img alt="img" src="forest_cm.png"/>
</div>
<div>
Случайный лес показал качество хуже более простых алгоритмов, возможно он требует больше данных для обучения.
</div>
</div>

---

# Нелинейные модели: XGBoost

Пайплайн для модели XGBoost включает в себя:
- TF-IDF векторизация текстов пресс-релизов
- XGBoost-классификатор

---

<style scoped>
    table, td, th {
        width: 100%;
    }
</style>

# XGBoost: метрики качества

<div class="container">
<div>

| Метрика     | Значение |
|-------------|----------|
| Accuracy    | 0.632353 |
| F1-score    | 0.633905 |
| Recall      | 0.625271 | 
| Precision   | 0.653274 |
| ROC-AUC OvR | 0.766337 |
| ROC-AUC OvO | 0.771152 |

</div>
<div class="item-img">
    <img alt="img" src="xgboost_cm.png"/>
</div>
<div>
XGBoost показал accuracy лучше других бустингов, но хуже более простых алгоритмов.
</div>
</div>

---

# Нелинейные модели: Catboost

Пайплайн для модели Catboost включает в себя:
- TF-IDF векторизация текстов пресс-релизов
- Catboost-классификатор

---

<style scoped>
    table, td, th {
        width: 100%;
    }
</style>

# Catboost: метрики качества

<div class="container">
<div>

| Метрика     | Значение |
|-------------|----------|
| Accuracy    | 0.514706 |
| F1-score    | 0.520886 |
| Recall      | 0.506572 | 
| Precision   | 0.571789 |
| ROC-AUC OvR | 0.701963 |
| ROC-AUC OvO | 0.709235 |

</div>
<div class="item-img">
    <img alt="img" src="catboost_cm.png"/>
</div>
<div>
Catboost показал качество хуже другх бустингов.
</div>
</div>

---

# Нелинейные модели: LigthGBM

Пайплайн для модели LigthGBM включает в себя:
- TF-IDF векторизация текстов пресс-релизов
- LigthGBM-классификатор

---

<style scoped>
    table, td, th {
        width: 100%;
    }
</style>

# LigthGBM: метрики качества

<div class="container">
<div>

| Метрика     | Значение |
|-------------|----------|
| Accuracy    | 0.588235 |
| F1-score    | 0.598482 |
| Recall      | 0.584844 | 
| Precision   | 0.637146 |
| ROC-AUC OvR | 0.789938 |
| ROC-AUC OvO | 0.796427 |

</div>
<div class="item-img">
    <img alt="img" src="lightgbm_cm.png"/>
</div>
<div>
LigthGBM показал качество ROC-AUC лучше, чем другие бустинги, но хуже более простых алгоритмов.
</div>
</div>

---

# Ансамбль из лучших моделей

В ансамбль методом обычного голосования мы включили следующие модели:
- SVC
- KNN
- TimeSeries (KNN)

---

<style scoped>
    table, td, th {
        width: 100%;
    }
</style>

# Ансамбль: метрики качества

<div class="container">
<div>

| Метрика     | Значение |
|-------------|----------|
| Accuracy    | 0.764706 |
| F1-score    | 0.767806 |
| Recall      | 0.766238 | 
| Precision   | 0.771946 |
| ROC-AUC OvR | 0.860113 |
| ROC-AUC OvO | 0.863595 |

</div>
<div class="item-img">
    <img alt="img" src="ensemble_cm.png"/>
</div>
<div>
Ансамбль показывает самую высокую метрику ROC-AUC-OvO среди всех моделей классического ML, которые мы поробовали.
</div>
</div>

---

# Метрики качества
<div class="metrics-container">
<div class="metrics-img">
    <img alt="img" src="metrics.png"/>
</div>
<div class="metrics-text">
Ансамбль превзошел по интегральным метрикам качества остальные модели, хотя его остальные метрики немного ниже чем у KNN.
</div>
</div>

---

# Выводы

- При подборе лучших моделей для ансамбля, заметили, что стоит смотреть не только на ROC-AUC-OvO, но также и на Accuracy.
- Методы ансамблирования моделей, такие как бустинг и случайный лес, окзались хуже более простых моделей, да и качество линейных алгоритмов с трудом удалось перебить. Виной этому небольшая выборка и значительное количество признаков - на порядок больше размера выборки.
- В связи с этим, методы PCA и отбор признаков с помощью L1-регуляризации оказали положительное влияние на качество моделей.
- Word2Vec и GloVe с нелинейными моделями показали плохой результат, как и в случае линейных, поскольку среднее от векторов слов плохо отражает смысл всего текста.