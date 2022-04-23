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

    def get_phrase_docs(self, phrase: list[str]):
        postings_list = self.dictionary[phrase[0]]
        for word in phrase[1:]:
            postings_list += 1
            postings_list = self.dictionary.get(word, PostingsList()) & postings_list

        result = {}
        for item in postings_list.list:
            if len(item) > 0:
                result[item.doc_id] = len(item)
        return result

    def get_all_except(self, phrase: list[str]):
        phrase_docs = self.get_phrase_docs(phrase)
        result = {}
        for key in self.dictionary:
            if key not in phrase_docs:
                result[key] = 0
        return result

    def get_phrase_except(self, phrase1: list[str], phrase2: list[str]):
        phrase1_docs = self.get_phrase_docs(phrase1)
        phrase2_docs = self.get_phrase_docs(phrase2)
        result = {}
        for key in phrase1_docs:
            if key not in phrase2_docs:
                result[key] = phrase1_docs[key]
        return result

    def get_phrase_and(self, phrase1: list[str], phrase2: list[str]):
        phrase1_docs = self.get_phrase_docs(phrase1)
        phrase2_docs = self.get_phrase_docs(phrase2)
        result = {}
        for key in phrase1_docs:
            if key in phrase2_docs:
                result[key] = min(phrase1_docs[key], phrase2_docs[key])
        return result

    def get_phrase_or(self, phrase1: list[str], phrase2: list[str]):
        phrase1_docs = self.get_phrase_docs(phrase1)
        phrase2_docs = self.get_phrase_docs(phrase2)
        result = phrase1_docs.copy()
        for key in phrase2_docs:
            if key in result:
                result[key] = max(result[key], phrase2_docs[key])
        return result

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
        return pd.Series(nonstop_tokens, dtype='object').apply(PositionalIndex.stemmer.convert_to_stem).values  # Getting stems

    def __str__(self):
        return str(self.dictionary)

    def __repr__(self):
        return str(self)
