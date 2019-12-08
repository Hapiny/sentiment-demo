import spacy
import os

from typing import List, Union, Tuple, Dict
from collections import defaultdict
from tqdm import tqdm
from models.utils import TRAIN_TEXTS, load_sentiment_data


class Tokenizer(object):
    def __init__(
        self, 
        _vocab_path: str = None,
        _load_sentiment_vocab: bool = False,
        _batch_size: int = 500
    ):
        self.nlp = spacy.load("en")
        self.vocab_path = _vocab_path
        self.use_sentiment_dict = _load_sentiment_vocab
        self.batch_size = _batch_size
        self.word2id = self.load_vocab(_load_sentiment_vocab)

    def tokenize(
        self, 
        sentences: List[str], 
        return_lemmas: bool = False,
        batch_size: int = 500
    ) -> Union[List[List[str]], Tuple[List[List[str]], List[List[str]]]]:
        tokens, lemmas = [], []
        text_processor = self.nlp.pipe(sentences,
                                       batch_size=batch_size,
                                       n_threads=4,
                                       disable=['ner', 'parser', 'tagger'])
        for doc in tqdm(text_processor, total=len(sentences)):
            tokens.append([token.text for token in doc])
            lemmas.append([token.lemma_ for token in doc])
        if return_lemmas:
            return tokens, lemmas
        else:
            return tokens
    
    def create_vocab(
        self,
        texts_path: str,
        save_path: str,
        min_df: Union[int, float] = 1,
        max_df: Union[int, float] = 1.0,
        stopwords: List[str] = None
    ) -> Dict[str, int]:
        def process_batch(batch, _token2freq):
            batch_of_tokens = self.tokenize(batch)
            for tokens in batch_of_tokens:
                for _token in tokens:
                    if stopwords and _token in stopwords:
                        continue
                    _token2freq[_token] += 1

        token2freq = defaultdict(int)
        number_of_documents = 0
        with open(texts_path, "r") as fp:
            lines = fp.readlines()
        batch_of_sentences = []
        for idx, line in tqdm(enumerate(lines, 1), desc=f"Creating vocab from {str(texts_path)}"):
            if not line.strip():
                continue
            number_of_documents += 1
            batch_of_sentences.append(line.strip())
            if idx % self.batch_size == 0:
                process_batch(batch_of_sentences, token2freq)
                batch_of_sentences = []
        if batch_of_sentences:
            process_batch(batch_of_sentences, token2freq)
        word2id = dict()
        if isinstance(min_df, float):
            min_df = int(min_df * number_of_documents)
        if isinstance(max_df, float):
            max_df = int(max_df * number_of_documents)
        for token, freq in token2freq.items():
            if min_df <= freq <= max_df:
                word2id[token] = len(word2id)
        with open(save_path, "r") as fp:
            for word in word2id:
                fp.write(word + "\n")
        return word2id

    def load_vocab(
        self,
        _load_sentiment_vocab
    ) -> Dict[str, int]:
        word2id = dict()
        if not _load_sentiment_vocab:
            if not os.path.exists(self.vocab_path):
                # Create vocab from train texts if it doesn't exist
                word2id = self.create_vocab(TRAIN_TEXTS, self.vocab_path)
            else:
                # Otherwise read it and create word2id
                word2id = dict()
                with open(self.vocab_path, "r") as fp:
                    for line in fp:
                        word = line.strip()
                        if word:
                            word2id[word] = len(word2id)
        else:
            sentiment_data = load_sentiment_data()
            for word in sorted(sentiment_data.word.unique().tolist()):
                word2id[word] = len(word2id)
        return word2id
