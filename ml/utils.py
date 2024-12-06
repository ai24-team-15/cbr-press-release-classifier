import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, f1_score, recall_score, \
    precision_score, roc_auc_score, confusion_matrix, classification_report




def calc_metrics(X, y, model, *, name, plot=True, **params):
    """
    Функция для тестирования наших моделей. 
    Зададим начальный порог и будем обучать, 
    модель на наблюдениях до порога, 
    а тестировать на одном наблюдении после. 
    Двигая порог протестируем нашу модель. 
    И потом сравним с истинными ответами. 
    Качество всех наших моделей будем записывать в metrics.csv
    """
    y_preds = []
    y_preds_proba = []
    model = model(**params)
    for threshold in range(30, 96):
        X_train = X[:threshold]
        X_test = X[threshold:]
        y_train = y[:threshold]

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test[0].reshape(1, -1))
        y_pred_proba = model.predict_proba(X_test[0].reshape(1, -1))
        y_preds.append(y_pred.item())
        y_preds_proba.append(y_pred_proba)

    acc = accuracy_score(y[30:], y_preds)
    f1 = f1_score(y[30:], y_preds, average='macro')
    recall = recall_score(y[30:], y_preds, average='macro')
    precision = precision_score(y[30:], y_preds, average='macro')
    roc_auc = roc_auc_score(y[30:], np.concatenate(y_preds_proba, axis=0), average='macro', multi_class='ovr')
    if plot:
        print(classification_report(y[30:], y_preds))
        cm = confusion_matrix(y[30:], y_preds)
        cm = pd.DataFrame(cm, index=['-1', '0', '1'], columns=['-1', '0', 1])
        sns.heatmap(cm, annot=True, fmt='d')
        plt.title("Confusion matrix")
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        plt.show()

        metrics = pd.DataFrame({
            'accuracy': acc, 'f1': f1, 'recall': recall, 'precision': precision, 'roc_auc_ovr': roc_auc,
            }, index=[name])
        return metrics, model
    else:
        return roc_auc.item(), model
    