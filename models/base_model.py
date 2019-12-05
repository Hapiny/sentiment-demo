from typing import Dict, List
from tqdm import tqdm
from pathlib import Path
from sklearn.metrics import accuracy_score
from datetime import datetime
import pandas as pd

from models.tokenizer import Tokenizer
from models.utils import SENTIMENT_DICT_PATH, TRAIN_TEXTS, DEV_TEXTS, TEST_TEXTS, \
    load_sentiment_data, TRAIN_LABELS, DEV_LABELS

PROJECT_PATH = Path(__file__).parent.parent


class BaseModel(object):
    def __init__(self):
        self.tokenizer = Tokenizer(_load_sentiment_vocab=True)
        self.word2sentiment = self.create_sentiment_mapping()

    def create_sentiment_mapping(
        self
    ) -> Dict[str, int]:
        sent_df = load_sentiment_data()
        word2sentiment = dict()
        for word in tqdm(self.tokenizer.word2id, desc="Creating sentiment mapping..."):
            positive_value = sent_df[(sent_df.word == word) & (sent_df.label == "positive")].value.tolist()[0]
            negative_value = sent_df[(sent_df.word == word) & (sent_df.label == "negative")].value.tolist()[0]
            if positive_value and not negative_value:
                word2sentiment[word] = "pos"
            elif negative_value and not positive_value:
                word2sentiment[word] = "neg"
        return word2sentiment

    def train(self, *args, **kwargs):
        raise NotImplementedError("Override this method in inhereted classes.")

    def predict(self, sentences: List[str]) -> List[Dict]:
        predicted = []
        all_tokens, all_lemmas = self.tokenizer.tokenize(sentences, return_lemmas=True)
        for tokens, lemmas in tqdm(zip(all_tokens, all_lemmas), desc="Predicting sentiment..."):
            response = {
                "label":    None,
                "features": []
            }
            score = 0
            for idx, lemma in enumerate(lemmas):
                if lemma not in self.word2sentiment:
                    response["features"].append([tokens[idx], 0])
                    continue
                lemma_sentiment = self.word2sentiment[lemma]
                if lemma_sentiment == "pos":
                    score += 1
                    response["features"].append([tokens[idx], 1])
                else:
                    score -= 1
                    response["features"].append([tokens[idx], -1])
                if score >= 0:
                    response["label"] = "pos"
                else:
                    response["label"] = "neg"
            predicted.append(response)
        return predicted

    def evaluate(
        self, 
        dataset_part: str,
        gold_lables_path: str = None,
        save_predictions: bool = False
    ):
        sentences_path = None
        if dataset_part == "train":
            sentences_path = TRAIN_TEXTS
            gold_lables_path = TRAIN_LABELS
        elif dataset_part == "dev":
            sentences_path = DEV_TEXTS
            gold_lables_path = DEV_LABELS
        else:
            raise ValueError(f"Invalid dataset part: {dataset_part}")
        with open(sentences_path, "r") as fp:
            sentences = [line.strip() for line in fp.readlines() if line.strip()]
        predicted = self.predict(sentences)
        with open(gold_lables_path, "r") as fp:
            gold_labels = [line.strip() for line in fp.readlines() if line.strip()]
        predicted_labels = [pred["label"] for pred in predicted]
        if save_predictions:
            data = {"sentence": sentences, "prediction": predicted_labels}
            pd.Dataframe(data=data).to_csv(f"base_model_{datetime.now().strfime('%d-%m %H:%M')}.csv", sep="\t", index=False)
        print(f"Accuracy: {accuracy_score(predicted_labels, gold_labels)}")


if __name__ == "__main__":
    model = BaseModel()
    model.evaluate("dev", save_predictions=True)