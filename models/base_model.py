from typing import Dict, List
from tqdm import tqdm
from pathlib import Path
from sklearn.metrics import accuracy_score
from datetime import datetime
import pandas as pd
import pickle

from models.tokenizer import Tokenizer
from models.utils import TRAIN_TEXTS, DEV_TEXTS, \
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
            num_positive_words, num_negative_words = 0, 0
            positive_features, negative_features = [], []
            for idx, lemma in enumerate(lemmas):
                if lemma not in self.word2sentiment:
                    response["features"].append([lemmas[idx], 0])
                    continue
                lemma_sentiment = self.word2sentiment[lemma]
                if lemma_sentiment == "pos":
                    score += 1
                    num_positive_words += 1
                    if len(positive_features) < 5:
                        positive_features.append([lemmas[idx], 1])
                    response["features"].append([lemmas[idx], 1])
                else:
                    score -= 1
                    num_negative_words += 1
                    if len(negative_features) < 5:
                        negative_features.append([lemmas[idx], -1])
                    response["features"].append([lemmas[idx], -1])
            
            response["pos_features"] = positive_features
            response["neg_features"] = negative_features
            
            if score > 0:
                response["label"] = "pos"
            else:
                response["label"] = "neg"

            positive_prob, negative_prob = 0.0, 0.0
            num_words = num_positive_words + num_negative_words
            if num_words == 0:
                positive_prob, negative_prob = 0.5, 0.5
            else:
                positive_prob = round(num_positive_words / num_words, 2)
                negative_prob = round(num_negative_words / num_words, 2)
            response["pos_prob"] = positive_prob
            response["neg_prob"] = negative_prob
            predicted.append(response)
        return predicted

    def evaluate(
        self, 
        dataset_part: str,
        save_predictions: bool = False,
        save_model: bool = False
    ):
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
        model_name = f"{self.__class__.__name__}_{datetime.now().strftime('%d_%m_%H:%M')}"
        if save_predictions:
            data = {"sentence": sentences, "prediction": predicted_labels}
            pd.DataFrame(data=data).to_csv(f"{model_name}.csv",
                                           sep="\t",
                                           index=False)
        if save_model:
            self.save_model(model_name)
        print(f"Accuracy on {dataset_part.title()}: {accuracy_score(predicted_labels, gold_labels)}")

    def save_model(self, save_file_path: str = None):
        if save_file_path is None:
            save_file_path = f"{self.__class__.__name__}_{datetime.now().strftime('%d_%m_%H:%M')}"
        save_file_path += ".sav"
        with open(save_file_path, "wb") as fp:
            pickle.dump(self, fp)


if __name__ == "__main__":
    model = BaseModel()
    model.evaluate("dev", save_predictions=False, save_model=True)
