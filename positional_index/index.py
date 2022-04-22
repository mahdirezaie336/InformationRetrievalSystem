from parsivar import Normalizer, Tokenizer, FindStems
from stopwordsiso import stopwords

from positional_index.postingslist import PostingsList
from positional_index.document import Document

import pandas as pd


class PositionalIndex:

    dictionary: dict[str, PostingsList]
    normalizer = Normalizer()
    tokenizer = Tokenizer()
    stemmer = FindStems()
    stop_words = stopwords('fa')

    def __init__(self):
        self.dictionary = {}
        self.documents = {}

    def add_token(self, term: str, document: Document, index: int):
        doc_id = document.id
        if term not in self.dictionary:
            self.dictionary[term] = PostingsList()
        self.dictionary[term].add_posting(doc_id, index)
        if doc_id not in self.documents:
            self.documents[doc_id] = document

    def add_tokens(self, term: str, document: Document, indices: list[int]):
        for index in indices:
            self.add_token(term, document, index)

    def add_document(self, document: Document):
        for i, token in enumerate(document.tokens):
            self.add_token(token, document, i)

    def add_from_dict(self, doc_id: str, docs: dict):
        document = Document.parse_from_dict(doc_id, docs)
        for i, token in enumerate(docs['tokens']):
            self.add_token(token, document, i)

    def check_phrase(self, phrase: list[str]):

        pass

    def query(self, query: str):
        words = PositionalIndex.preprocess(query)

    @staticmethod
    def preprocess(text: str):
        normalized_text = PositionalIndex.normalizer.normalize(text)        # Normalization
        tokens = PositionalIndex.tokenizer.tokenize_words(normalized_text)  # Tokenization
        nonstop_tokens = []                                                 # Handling stop words
        for token in tokens:
            if token not in PositionalIndex.stop_words:
                nonstop_tokens.append(token)
        return pd.Series(nonstop_tokens).apply(PositionalIndex.stemmer.convert_to_stem).values  # Getting stems

    def __str__(self):
        return str(self.dictionary)

    def __repr__(self):
        return str(self)
