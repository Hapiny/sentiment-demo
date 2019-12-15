from itertools import groupby
from typing import List, Dict, NoReturn

from models.base_model import BaseModel
from models.sklearn_tokenizer import Tokenizer
from models.utils import TRAIN_TEXTS, TRAIN_LABELS

from sklearn.linear_model import LogisticRegression


class LogisticRegressionModel(BaseModel):
    def __init__(
            self,
            verbose: bool = False
    ):
        super(LogisticRegressionModel, self).__init__()
        self.log_reg = LogisticRegression(
            C=0.05,
            n_jobs=4,
            verbose=verbose
        )
        self.tokenizer = Tokenizer(ngram_range=(1, 2))

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
        self.log_reg.fit(train_x, train_y)

    def predict(self, sentences: List[str]) -> List[Dict]:
        predicted = []
        transformed_texts = self.tokenizer.transform(sentences)
        row_ids, col_ids = transformed_texts.nonzero()
        row_col_pairs = sorted(zip(row_ids, col_ids), key=lambda x: x[0])
        row2cols = {
            row_idx: [col for _, col in columns]
            for row_idx, columns in groupby(row_col_pairs, key=lambda x: x[0])
        }
        prediction = self.log_reg.predict_proba(transformed_texts)
        for sample_idx, probs in enumerate(prediction):
            negative_prob, positive_prob = probs
            features = []
            positive_features, negative_features = [], []
            if sample_idx in row2cols:
                word_ids = row2cols[sample_idx]
                for idx in word_ids:
                    word = self.tokenizer.id2word[idx]
                    weight = self.log_reg.coef_[0, idx]
                    if weight >= 0:
                        positive_features.append([word, round(weight, 4)])
                    else:
                        negative_features.append([word, round(weight, 4)])
                    features.append([word, weight])
            predicted.append({
                "label": ("pos" if negative_prob < positive_prob else "neg"),
                "features": features,
                "pos_prob": round(positive_prob, 2),
                "neg_prob": round(negative_prob, 2),
                "pos_features": sorted(positive_features, key=lambda x: x[1], reverse=True)[:5],
                "neg_features": sorted(negative_features, key=lambda x: x[1])[:5]
            })
        return predicted


if __name__ == "__main__":
    model = LogisticRegressionModel()
    model.train()
    model.evaluate("dev", save_predictions=False, save_model=True)
