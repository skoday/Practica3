from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import re
import numpy as np

class Create_model:

    """
    THis class is intendede to create the specified model with the desired characteristics
    and return the model itself to work over it later on
    """

    def __init__(self, corpus: pd.DataFrame) -> None:
        """
        Only send normalized corpuses
        """
        self.corpus = corpus.copy()
        # Just adds an extra columns with 2 columns merged
        self.corpus["Título-Contenido"] = self.corpus["Título"] + " - " + self.corpus["Contenido"]
        self.token_pattern = r'\w+|[^\w\s]|\d+(?:\.\d+)?%?'

    """
    The following 3 functions create the model using the desidred column
    """
    def binary(self, ngram:int, column: str):
        binary_vectorizer = CountVectorizer(binary=True, token_pattern=self.token_pattern, ngram_range = (ngram,ngram))
        return binary_vectorizer.fit(self.corpus[column])

    def frequency(self, ngram:int, column: str):
        frequency_vectorizer = CountVectorizer(token_pattern=self.token_pattern, ngram_range = (ngram,ngram))
        return frequency_vectorizer.fit(self.corpus[column])

    def tfidf(self, ngram:int, column: str):
        tfidf__vectorizer = TfidfVectorizer(token_pattern=self.token_pattern, ngram_range = (ngram,ngram))
        return tfidf__vectorizer.fit(self.corpus[column])
    
class Adjust_Document:

    def __init__(self, model, documet, corpus, column) -> None:
        """
        Parameters:
        * Codel: model already fitted
        * Document: documetn we look similarities for
        * Corpus: all documents we are going to compare to
        * column: chosen column to co compare to
        """
        self.model = model
        self.document = documet
        self.corpus = corpus
        self.corpus["Título-Contenido"] = self.corpus["Título"] + " - " + self.corpus["Contenido"]
        self.column = column
        self.corpus_features = model.transform(self.corpus[column]) #self corpues es un Dframe
        self.document_features = model.transform(self.document["Documento"]) # Documets can be a list

        

    def compare(self):

        # Contains as many dataframes as documents
        compared_info = []

        for element in self.document_features.toarray():

            corpus_ws = self.corpus.copy()

            similarities = []
            for i in self.corpus_features.toarray():
                x = np.array(element).reshape(1, -1)
                y = np.array(i).reshape(1, -1)
                similarities.append(cosine_similarity(x, y)[0][0])
            corpus_ws["Similarity"] = similarities
            corpus_ws.sort_values(by='Similarity', ascending=False, inplace=True)
            compared_info.append(corpus_ws.head(10))

        return compared_info