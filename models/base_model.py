from typing import Dict, List
from tqdm import tqdm
from pathlib import Path
from sklearn.metrics import accuracy_score
from datetime import datetime
import pandas as pd

from models.tokenizer import Tokenizer
from models.utils import TRAIN_TEXTS, DEV_TEXTS, TEST_TEXTS, \
    load_sentiment_data, TRAIN_LABELS, DEV_LABELS

PROJECT_PATH = Path(__file__).parent.parent


class BaseModel(object):
    def __init__(self):
        self.tokenizer = Tokenizer(_load_sentiment_vocab=True)
        self.word2sentiment = self.create_sentiment_mapping()

    @staticmethod
    def create_sentiment_mapping() -> Dict[str, str]:
        sent_df = load_sentiment_data()
        word2sentiment = dict()
        positive_words = set(sent_df[(sent_df.label == "positive") & (sent_df.value == 1)].word.tolist())
        joy_words = set(sent_df[(sent_df.label == "joy") & (sent_df.value == 1)].word.tolist())
        positive_words |= joy_words

        negative_words = set(sent_df[(sent_df.label == "negative") & (sent_df.value == 1)].word.tolist())
        anger_words = set(sent_df[(sent_df.label == "anger") & (sent_df.value == 1)].word.tolist())
        disgust_words = set(sent_df[(sent_df.label == "disgust") & (sent_df.value == 1)].word.tolist())
        negative_words |= anger_words
        negative_words |= disgust_words

        common_words = positive_words & negative_words
        positive_words = positive_words - common_words
        negative_words = negative_words - common_words

        for word in positive_words:
            word2sentiment[word] = "pos"
        for word in negative_words:
            word2sentiment[word] = "neg"
        return word2sentiment

    def train(self, *args, **kwargs):
        raise NotImplementedError("Override this method in inherited classes.")

    def predict(self, sentences: List[str]) -> List[Dict]:
        predicted = []
        all_tokens, all_lemmas = self.tokenizer.tokenize(sentences, return_lemmas=True)
        for tokens, lemmas in tqdm(zip(all_tokens, all_lemmas), desc="Predicting sentiment...", total=len(sentences)):
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
        save_predictions: bool = False
    ):
        sentences_path = None
        if dataset_part == "train":
            sentences_path = TRAIN_TEXTS
            gold_labels_path = TRAIN_LABELS
        elif dataset_part == "dev":
            sentences_path = DEV_TEXTS
            gold_labels_path = DEV_LABELS
        else:
            raise ValueError(f"Invalid dataset part: {dataset_part}")
        with open(sentences_path, "r") as fp:
            sentences = [line.strip() for line in fp.readlines() if line.strip()]
        predicted = self.predict(sentences)
        with open(gold_labels_path, "r") as fp:
            gold_labels = [line.strip() for line in fp.readlines() if line.strip()]
        predicted_labels = [pred["label"] for pred in predicted]
        if save_predictions:
            data = {"sentence": sentences, "prediction": predicted_labels}
            model_name = self.__class__.__name__
            pd.DataFrame(data=data).to_csv(f"{model_name}_{datetime.now().strftime('%d-%m %H:%M')}.csv",
                                           sep="\t",
                                           index=False)
        print(f"Accuracy: {accuracy_score(predicted_labels, gold_labels)}")


if __name__ == "__main__":
    model = BaseModel()
    model.evaluate("dev", save_predictions=True)
