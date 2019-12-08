from pathlib import Path
from typing import List, Callable
import string
from concurrent.futures import ThreadPoolExecutor

import pandas as pd

# Project paths
DATA_DIR = Path(__file__).parent.parent / "data"
IMDB_DIR = DATA_DIR / "imdb"
STOPWORDS_PATH = IMDB_DIR / "stopwords.txt"
SENTIMENT_DICT_PATH = DATA_DIR / "sentiment_dict" / "sentiment-wordlevel.txt"
PUNCTUATION = string.punctuation

# Paths to files with sentences
TRAIN_TEXTS = IMDB_DIR / "train.texts"
DEV_TEXTS = IMDB_DIR / "dev.texts"
TEST_TEXTS = IMDB_DIR / "test.texts"

# Paths to files with labels for each sentence
TRAIN_LABELS = IMDB_DIR / "train.labels"
DEV_LABELS = IMDB_DIR / "dev.labels"


def load_sentiment_data() -> pd.DataFrame:
    sentiment_data = pd.read_csv(SENTIMENT_DICT_PATH, sep="\t", names=["word", "label", "value"])
    sentiment_data = sentiment_data.dropna()
    return sentiment_data


def parallel_requests(num_threads: int, task: Callable, args: List):
    response = []
    with ThreadPoolExecutor(max_workers=num_threads) as pool:
        response_iterator = pool.map(task, args)
        for res, model in zip(response_iterator, args):
            res_json = []
            try:
                res_json = res.json()
            except:
                print(f"Model {model} failed!")
            response.append(res_json)
    return response
