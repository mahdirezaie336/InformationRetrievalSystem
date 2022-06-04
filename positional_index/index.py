import math

import numpy as np
import heapq
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
    stop_words = stopwords('fa').difference('!')
    operations = {'"', '&', '|', '!', '&!'}

    def __init__(self):
        self.dictionary = {}
        self.documents = {}
        self.documents_df = pd.DataFrame(columns=['title', 'content', 'tags', 'date', 'url', 'category'])

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
        postings_list = self.dictionary.get(phrase[0], PostingsList())
        for word in phrase[1:]:
            postings_list += 1
            postings_list = self.dictionary.get(word, PostingsList()) & postings_list

        result = {}
        for item in postings_list.list:
            if len(item) > 0:
                result[item.doc_id] = len(item)
        return result

    def get_all_except(self, phrase):
        phrase_docs = self.get_phrase_docs(phrase) if type(phrase) == list else phrase
        result = {}
        for key in self.dictionary:
            if key not in phrase_docs:
                result[key] = 1
        return result

    def get_phrase_except(self, phrase1, phrase2):
        phrase1_docs = self.get_phrase_docs(phrase1) if type(phrase1) == list else phrase1
        phrase2_docs = self.get_phrase_docs(phrase2) if type(phrase2) == list else phrase2
        result = {}
        for key in phrase1_docs:
            if key not in phrase2_docs:
                result[key] = phrase1_docs[key]
        return result

    def get_phrase_and(self, phrase1, phrase2):
        phrase1_docs = self.get_phrase_docs(phrase1) if type(phrase1) == list else phrase1
        phrase2_docs = self.get_phrase_docs(phrase2) if type(phrase2) == list else phrase2
        result = {}
        for key in phrase1_docs:
            if key in phrase2_docs:
                result[key] = min(phrase1_docs[key], phrase2_docs[key])
        return result

    def get_phrase_or(self, phrase1, phrase2):
        phrase1_docs = self.get_phrase_docs(phrase1) if type(phrase1) == list else phrase1
        phrase2_docs = self.get_phrase_docs(phrase2) if type(phrase2) == list else phrase2
        result = phrase1_docs.copy()
        for key in phrase2_docs:
            if key in result:
                result[key] = max(result[key], phrase2_docs[key])
        return result

    def query(self, query: str):
        words = PositionalIndex.preprocess(query)
        stack = []
        for i, word in enumerate(words):
            # if the word is not an operation
            if word not in PositionalIndex.operations:
                if len(stack) == 0:
                    n = self.get_phrase_docs([word])
                    stack.append(n)
                else:
                    n = self.get_phrase_and(stack.pop(), [word])
                    stack.append(n)
            # If the word is an operation
            else:
                if word == '"':
                    j = None
                    for j, word2 in enumerate(words[i+1:]):
                        if word2 == '"':
                            break
                    phrase = words[i+1:j+i+1]
                    phrase_docs = self.get_phrase_docs(phrase)
                    if len(stack) == 0:
                        stack.append(phrase_docs)
                    else:
                        n = self.get_phrase_and(stack.pop(), phrase_docs)
                        stack.append(n)
                    del words[i: i+j+2]
                elif word == '&':
                    n = self.get_phrase_and(stack.pop(), [words[i+1]])
                    stack.append(n)
                    del words[i:i+2]
                elif word == '|':
                    n = self.get_phrase_or(stack.pop(), [words[i+1]])
                    stack.append(n)
                    del words[i:i+2]
                elif word == '!':
                    if len(stack) == 0:
                        n = self.get_all_except([words[i+1]])
                    else:
                        n = self.get_phrase_except(stack.pop(), [words[i+1]])
                    stack.append(n)
                    del words[i:i+2]
                elif word == '&!':
                    n = self.get_phrase_except(stack.pop(), [words[i+1]])
                    stack.append(n)
                    del words[i:i+2]
        s = pd.Series(stack[0], name='rank').to_frame()
        df = s.merge(self.documents_df, left_index=True, right_index=True)
        df.sort_values(by='rank', ascending=False, inplace=True)
        return df.loc[:, ["title", "url", "rank"]]

    def finish_indexing(self):
        r = []
        for doc_id in self.documents:
            document = self.documents[doc_id]
            s = pd.Series(document.to_dict(), name=document.id).to_frame().T
            r.append(s)
        self.documents_df = pd.concat(r)

    def get_term_weight(self, term: str, doc_id: int):
        if term not in self.dictionary:
            return 0

        postings_list = self.dictionary[term]
        n = len(self.documents)
        tf = np.log(1 + postings_list.get_term_frequency(doc_id))
        idf = np.log2(n) - np.log10(postings_list.get_document_frequency())
        return tf * idf

    def get_cosine_similarity(self, doc1, doc2: Document, query=True):
        ab = 0
        a2 = 0
        b2 = 0

        if not query:
            for token in doc1.tokens:
                w1 = self.get_term_weight(token, doc1.id)
                w2 = self.get_term_weight(token, doc2.id)
                if token in doc2.tokens:
                    ab += w1 * w2
                a2 += w1 * w1
        else:
            for token in doc1:
                doc1: list
                postings_list = self.dictionary[token]
                n = len(self.documents)
                tf = np.log(1 + doc1.count(token))
                idf = np.log2(n) - np.log10(postings_list.get_document_frequency())
                w1 = tf * idf
                w2 = self.get_term_weight(token, doc2.id)
                if token in doc2.tokens:
                    ab += w1 * w2
                a2 += w1 * w1

        for token in doc2.tokens:
            w2 = self.get_term_weight(token, doc2.id)
            b2 += w2 * w2

        # Handling divide by zero
        if a2 == 0 or b2 == 0:
            return 0.0

        return ab / (np.sqrt(a2) * np.sqrt(b2))

    def ranked_query(self, query: str, k_best=10):
        query_as_doc = PositionalIndex.preprocess(query)
        result = []
        for doc_id in self.documents:
            doc = self.documents[doc_id]
            result.append((doc_id, self.get_cosine_similarity(query_as_doc, doc, query=True)))
        result = np.array(result)

        # Handling k > len(docs) error
        if k_best > len(result):
            k_best = len(result)

        # Finding k-best result
        arg_result = result[:, 1].argpartition(-1 * k_best)[-1 * k_best:]
        similarity = pd.Series(data=result[arg_result, 1], index=result[arg_result, 0], name="similarity")
        df = self.documents_df.merge(similarity, right_index=True, left_index=True)
        return df.loc[arg_result, ["title", "url", "similarity"]].sort_values(by="similarity", ascending=False)

    def ranked_query_fast(self, query: str):
        pass

    @staticmethod
    def preprocess(text: str):
        normalized_text = PositionalIndex.normalizer.normalize(text)        # Normalization
        tokens = PositionalIndex.tokenizer.tokenize_words(normalized_text)  # Tokenization
        nonstop_tokens = []                                                 # Handling stop words
        for token in tokens:
            if token not in PositionalIndex.stop_words:
                nonstop_tokens.append(token)
        return pd.Series(nonstop_tokens, dtype='object')\
            .apply(PositionalIndex.stemmer.convert_to_stem)\
            .values.tolist()                                                # Getting stems

    def __str__(self):
        return str(self.dictionary)

    def __repr__(self):
        return str(self)
