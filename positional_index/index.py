from postingslist import PostingsList
from document import Document


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
