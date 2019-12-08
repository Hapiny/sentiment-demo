from typing import Union, Tuple, List
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import CountVectorizer

from models.utils import TRAIN_TEXTS


class Tokenizer(object):
    def __init__(
            self,
            min_df: Union[int, float] = 2,
            max_df: Union[int, float] = 1.0,
            use_stop_words: bool = True,
            ngram_range: Tuple = (1, 1),
            max_features: int = 200000
    ):
        super(Tokenizer, self).__init__()
        stop_words = ("english" if use_stop_words else None)
        self.vectorizer = CountVectorizer(min_df=min_df,
                                          max_df=max_df,
                                          stop_words=stop_words,
                                          ngram_range=ngram_range,
                                          max_features=max_features)
        with open(TRAIN_TEXTS, "r") as fp:
            sentences = [line.strip() for line in fp if line.strip()]
        self.vectorizer.fit(sentences)
        self.word2id = self.vectorizer.vocabulary_
        self.id2word = {idx: word for word, idx in self.word2id.items()}

    def transform(
            self,
            sentences: List[str]
    ) -> csr_matrix:
        sparse_matrix = self.vectorizer.transform(sentences)
        return sparse_matrix
