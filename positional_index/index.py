from positional_index.postingslist import PostingsList
from positional_index.document import Document


class PositionalIndex:

    dictionary: dict[str, PostingsList]

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
        document = Document.parse_from_dict(docs)
        for i, token in enumerate(docs['tokens']):
            self.add_token(token, document, i)

    def query(self):
        pass

    def __str__(self):
        return str(self.dictionary)

    def __repr__(self):
        return str(self)
