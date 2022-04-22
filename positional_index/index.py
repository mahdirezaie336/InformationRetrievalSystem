from positional_index.postingslist import PostingsList
from positional_index.document import Document


class PositionalIndex:

    dictionary: dict[str, PostingsList]

    def __init__(self):
        self.dictionary = {}

    def add_token(self, term: str, doc_id: int, index: int):
        if term not in self.dictionary:
            self.dictionary[term] = PostingsList()
        self.dictionary[term].add_posting(doc_id, index)

    def add_tokens(self, term: str, doc_id: int, indices: list[int]):
        for index in indices:
            self.add_token(term, doc_id, index)

    def add_document(self, document: Document):
        for i, token in enumerate(document.tokens):
            self.add_token(token, document.id, i)

    def add_from_dict(self, doc_id: str, docs: dict):
        for i, token in enumerate(docs['tokens']):
            self.add_token(token, int(doc_id), i)

    def __str__(self):
        return str(self.dictionary)

    def __repr__(self):
        return str(self)
