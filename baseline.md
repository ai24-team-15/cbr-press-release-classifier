## Построение бейзлайна

Цель данной работы построение бейзлайна и его улучшение с помощью простейших моделей, для предсказания направления изменения ставки рефинансирования ЦБ. Это наша отправная точка для сравнения и улучшения.

### План работы

0. Общая предобработка данных.
1. Минимальный бейзлайн.
2. Статистические методы :
    - Мешок слов плюс линейная модель
    - TF-IDF плюс линейная модель
    - N-граммы плюс Naive Bayes
3. Создание эмбеддингов:
    - Word2Vec плюс линейная модель
    - GloVe плюс линейная модель
4. Выводы

### Ноутбуки с экспериментами

- [min_baseline.ipynb](ml/linear_models/min_baseline.ipynb) - минимальный бейзлайн. Модель предсказывает изменение ставки таким, как в последнем решении.
- [dummy.ipynb](ml/linear_models/dummy.ipynb) - простейшее предсказание на основе самого частотного класса (вне рейтинга).
- [bag_of_words.ipynb](ml/linear_models/bag_of_words.ipynb) - Bag of Words плюс линейные модели (логистическая регрессия регрессия и SVM).
- [tf_idf.ipynb](ml/linear_models/tf_idf.ipynb) - TF-IDF плюс линейные модели. Здесь была получена наилучшая модель.
- [n_grams_naive_bayes.ipynb](ml/linear_models/n_grams_naive_bayes.ipynb) - N-граммы плюс наивный байесовский классификатор.
- [word2vec.ipynb](ml/linear_models/word2vec.ipynb) - Word2Vec плюс линейная модель.
- [glove.ipynb](ml/linear_models/glove.ipynb) - GloVe плюс линейная модель.
- [pipeline.ipynb](ml/linear_models/pipeline.ipynb) - пайплайн обучения и применения лучшей модели (TF-IDF + SVM).

### Метрики исследованных моделей

<table border="1" class="dataframe">
  <thead>
    <tr>
      <th>Модель</th>
      <th>Accuracy</th>
      <th>F-score</th>
      <th>Precision</th>
      <th>Recall</th>
      <th>ROC AUC OvR</th>
      <th>ROC AUC OvO</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Минимальный бейзлайн</th>
      <td>0.659794</td>
      <td>0.664127</td>
      <td>0.664127</td>
      <td>0.664127</td>
      <td>0.742845</td>
      <td>0.748095</td>
    </tr>
    <tr>
      <th>BoW (тексты релизов) + LogReg с L1-регуляризацией</th>
      <td>0.617647</td>
      <td>0.623226</td>
      <td>0.633465</td>
      <td>0.617174</td>
      <td>0.764882</td>
      <td>0.770478</td>
    </tr>
    <tr>
      <th>BoW + LogReg с L1-, L2-регуляризацией</th>
      <td>0.602941</td>
      <td>0.606085</td>
      <td>0.617424</td>
      <td>0.599630</td>
      <td>0.779381</td>
      <td>0.783093</td>
    </tr>
    <tr>
      <th>BoW (тексты релизов + заголовки) + LogReg</th>
      <td>0.573529</td>
      <td>0.579365</td>
      <td>0.591162</td>
      <td>0.572317</td>
      <td>0.782876</td>
      <td>0.786569</td>
    </tr>
    <tr>
      <th>BoW (тексты релизов + числовые переменные) + LogReg</th>
      <td>0.573529</td>
      <td>0.579365</td>
      <td>0.591162</td>
      <td>0.572317</td>
      <td>0.776894</td>
      <td>0.781362</td>
    </tr>
    <tr>
      <th>BoW (тексты релизов) + SVM</th>
      <td>0.632353</td>
      <td>0.641077</td>
      <td>0.650132</td>
      <td>0.634718</td>
      <td>0.784936</td>
      <td>0.790207</td>
    </tr>
    <tr>
      <th>TF-IDF (тексты релизов) + LogReg с L1-регуляризацией</th>
      <td>0.617647</td>
      <td>0.617077</td>
      <td>0.625831</td>
      <td>0.615795</td>
      <td>0.784421</td>
      <td>0.789606</td>
    </tr>
    <tr>
      <th>TF-IDF (тексты релизов c доп. фильтрацией) + LogReg</th>
      <td>0.720588</td>
      <td>0.722979</td>
      <td>0.737452</td>
      <td>0.716658</td>
      <td>0.808578</td>
      <td>0.813516</td>
    </tr>
    <tr>
      <th>TF-IDF (тексты релизов + заголовки) + LogReg</th>
      <td>0.705882</td>
      <td>0.710449</td>
      <td>0.727536</td>
      <td>0.702165</td>
      <td>0.811914</td>
      <td>0.816596</td>
    </tr>
    <tr>
      <th>TF-IDF (тексты релизов + числовые переменные) + LogReg</th>
      <td>0.632353</td>
      <td>0.636409</td>
      <td>0.687037</td>
      <td>0.621927</td>
      <td>0.774436</td>
      <td>0.776844</td>
    </tr>
    <tr style="background-color: yellow;">
      <th>TF-IDF (тексты релизов) + SVM</th>
      <td>0.691176</td>
      <td>0.693718</td>
      <td>0.700864</td>
      <td>0.691017</td>
      <td>0.840529</td>
      <td>0.844115</td>
    </tr>
    <tr>
      <th>N-граммы плюс Naive Bayes</th>
      <td>0.632353</td>
      <td>0.627996</td>
      <td>0.625522</td>
      <td>0.644458</td>
      <td>0.763456</td>
      <td>0.769950</td>
    </tr>
    <tr>
      <th>Word2Vec + LogReg</th>
      <td>0.588235</td>
      <td>0.592543</td>
      <td>0.591519</td>
      <td>0.597929</td>
      <td>0.749491</td>
      <td>0.754650</td>
    </tr>
    <tr>
      <th>Word2Vec (предобученная модель) + LogReg</th>
      <td>0.588235</td>
      <td>0.602646</td>
      <td>0.617677</td>
      <td>0.592912</td>
      <td>0.752914</td>
      <td>0.759887</td>
    </tr>
    <tr>
      <th>Word2Vec (предобученная модель) + SVM</th>
      <td>0.558824</td>
      <td>0.568687</td>
      <td>0.577233</td>
      <td>0.562548</td>
      <td>0.708429</td>
      <td>0.716086</td>
    </tr>
    <tr>
      <th>GloVe + LogReg</th>
      <td>0.647059</td>
      <td>0.653199</td>
      <td>0.661626</td>
      <td>0.647539</td>
      <td>0.763768</td>
      <td>0.770111</td>
    </tr>
  </tbody>
</table>

### Выводы

В качестве бейзлайна построена модель, которая возвращает в качестве прогноза предыдущее решение о ставке рефинансирования.

Метрикой качества для сравнения моделей была выбрана ROC AUC OvO, поскольку она является интегральной (не зависит от порога перевода вероятностей в классы), а также не чувствительна к дисбалансу классов (в нашем датасете наблюдается небольшой дисбаланс).

В ходе экспериментов было исследовано несколько улучшений базовой модели. Наилучший результат среди них показала модель с векторизацией TF-IDF текстов релизов плюc SVM. Добавление дополнительной информации (заголовков, числовых переменных) не улучшало модели.

Алгоритмы Word2Vec и GloVe показали качество хуже, поскольку они неплохо создают представления слов, но в сумме этих представлений плохо сохраняется смысл всего текста.

Так же алгоритмы Word2Vec, GloVe демонстрируют низкие показатели, что возможно связано с размером выборки, который недостаточен для успешного обучения или плохо учитывает корреляцию между признаками. 

