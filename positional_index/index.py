from postingslist import PostingsList


class PositionalIndex:

    dictionary: dict[str, PostingsList]

    def __init__(self):
        self.dictionary = {}

    def add_token(self, term: str, doc_id: int, index: int):
        if term in self.dictionary:
            self.dictionary[term].add_posting(doc_id)

