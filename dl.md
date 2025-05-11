Ни одна из DL-моделей не смогла превзойти по качеству лучшую линейную модель. Ноутбуки с экспериментами:

- [Классический многослойный перцептрон](ml/dl_models/mlp.ipynb)
- [Сверточные сети](ml/dl_models/cnn.ipynb)
- [Sentence Transformer](ml/dl_models/sentence_transformer.ipynb)
- [Sentence Transformer без ограничения длины текста](ml/dl_models/sentence_transformer_chunk.ipynb)

### Сравнение метрик

В таблице представлены лучшие результаты моделей разных типов.

<table>
    <tr>
        <th>Модель</th>
        <th>Accuracy</th>
        <th>ROC AUC OvO</th>
    </tr>
    <tr>
        <td>Бейзлайн: последнее известное значение</td>
        <td>0.6667</td>
        <td>0.7524</td>
    </tr>
    <tr>
        <td>Лучшая линейная модель: TF-IDF + SVC</td>
        <td>0.7143</td>
        <td>0.8535</td>
    </tr>
    <tr>
        <td>Лучшая нелинейная модель: TF-IDF + KNN</td>
        <td>0.7429</td>
        <td>0.8441</td>
    </tr>
    <tr>
        <td>Ансамбль классических моделей (TF-IDF + генерация признаков + SVC + KNN)</td>
        <td>0.7428</td>
        <td>0.8496</td>
    </tr>
    <tr>
        <td>Лучшая DL-модель: Sentence transformer</td>
        <td>0.6571</td>
        <td>0.8319</td>
    </tr>
</table>

По совокупности метрик наилучший результат показывает ансамбль классических моделей (практически такая же доля правильных ответов, как у KNN, но метрика ROC AUC ансамбля выше).
