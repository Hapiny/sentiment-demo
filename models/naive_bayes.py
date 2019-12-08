import numpy as np
from typing import List, Dict, NoReturn
from itertools import groupby

from models.base_model import BaseModel
from models.sklearn_tokenizer import Tokenizer
from models.utils import TRAIN_TEXTS, TRAIN_LABELS

from sklearn.naive_bayes import MultinomialNB, BernoulliNB


class NaiveBayesModel(BaseModel):
    def __init__(
            self,
            _type: str = "multinomial"
    ):
        super(NaiveBayesModel, self).__init__()
        self.bayes_type = _type
        self.bayes = self.create_bayes()
        self.tokenizer = Tokenizer()

    def create_bayes(self):
        if self.bayes_type == "multinomial":
            return MultinomialNB()
        elif self.bayes_type == "bernoulli":
            return BernoulliNB()
        else:
            raise ValueError(f"Invalid bayes type: {self.bayes_type}")

    def train(
            self,
            train_texts: List[str] = None,
            train_labels: List[str] = None
    ) -> NoReturn:
        if train_texts is None:
            with open(TRAIN_TEXTS, "r") as fp:
                train_texts = [line.strip() for line in fp if line.strip()]

        if train_labels is None:
            with open(TRAIN_LABELS, "r") as fp:
                train_labels = [line.strip() for line in fp if line.strip()]
        assert len(train_texts) == len(train_labels), \
            f"Train texts and labels must be the same length. " \
            f"({len(train_texts)}, {len(train_labels)})"
        train_x = self.tokenizer.transform(train_texts)
        train_y = [1 if label == "pos" else 0 for label in train_labels]
        self.bayes.fit(train_x, train_y)

    def predict(self, sentences: List[str]) -> List[Dict]:
        predicted = []
        transformed_texts = self.tokenizer.transform(sentences)
        row_ids, col_ids = transformed_texts.nonzero()
        row_col_pairs = sorted(zip(row_ids, col_ids), key=lambda x: x[0])
        row2cols = {
            row_idx: [col for _, col in columns]
            for row_idx, columns in groupby(row_col_pairs, key=lambda x: x[0])
        }
        feature_count_matrix = self.bayes.feature_count_
        feature_count_matrix = feature_count_matrix / feature_count_matrix.sum(axis=0, keepdims=True)
        prediction = self.bayes.predict_proba(transformed_texts)
        for sample_idx, probs in enumerate(prediction):
            features = []
            if sample_idx in row2cols:
                word_ids = row2cols[sample_idx]
                for idx in word_ids:
                    word = self.tokenizer.id2word[idx]
                    neg_weight = feature_count_matrix[0, idx]
                    pos_weight = feature_count_matrix[1, idx]
                    features.append([word, neg_weight, pos_weight])
            negative_prob, positive_prob = probs
            predicted.append({
                "label": ("pos" if negative_prob < positive_prob else "neg"),
                "features": features
            })
        return predicted


if __name__ == "__main__":
    model = NaiveBayesModel(_type="bernoulli")
    model.train()
    model.evaluate("dev", save_predictions=True)
