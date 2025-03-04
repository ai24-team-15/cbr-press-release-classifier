from sklearn.base import BaseEstimator, TransformerMixin, defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import word2vec
import numpy as np


class Word2VecVectorizer(BaseEstimator, TransformerMixin):
    """
    Формирует индекс word2vec для набора текстов.
    Возвращает вектор для текста как среднее векторов слов.
    """
    def __init__(self, *, preprocessor=None, **w2v_params):
        self.preprocessor = preprocessor
        self.w2v_params = w2v_params
    
    def fit(self, X, y=None):
        if self.preprocessor:
            X = X.apply(self.preprocessor).str.split().tolist()
        
        self.model = word2vec.Word2Vec(X, **self.w2v_params)
        
        return self
    
    def transform(self, X):
        if self.preprocessor:
            X = X.apply(self.preprocessor).str.split().tolist()

        zero = [np.zeros(self.model.vector_size)]
        return np.array([
            np.mean([self.model.wv[w] for w in words if w in self.model.wv] or zero, axis=0)
            for words in X
        ])
    

class Word2VecTfIdfVectorizer(BaseEstimator, TransformerMixin):
    """
    Формирует индекс word2vec для набора текстов.
    Возвращает вектор для текста как среднее векторов слов, взвешенных по мере TF-IDF (важности).
    """
    def __init__(self, *, preprocessor=None, **w2v_params):
        self.preprocessor = preprocessor
        self.w2v_params = w2v_params
    
    def fit(self, X, y=None, **tfidf_params):
        if self.preprocessor:
            X = X.apply(self.preprocessor).str.split().tolist()

        tfidf = TfidfVectorizer(analyzer=lambda x: x, **tfidf_params)
        tfidf.fit(X)

        max_idf = max(tfidf.idf_)
        self.word2weight = defaultdict(
            lambda: max_idf,
            [(w, tfidf.idf_[i]) for w, i in tfidf.vocabulary_.items()])
        
        self.model = word2vec.Word2Vec(X, **self.w2v_params)
        
        return self
    
    def transform(self, X):
        if self.preprocessor:
            X = X.apply(self.preprocessor).str.split().tolist()

        zero = [np.zeros(self.model.vector_size)]
        return np.array([
            np.mean([self.model.wv[w] * self.word2weight[w] for w in words if w in self.model.wv] or zero, axis=0)
            for words in X
        ])
