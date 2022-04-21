from document import Document

class Item:

    def __init__(self, document: Document):
        self.document = document
        self.indices = []

    def add_index(self, index):
        for i, item in enumerate(self.indices[::-1]):
            if index >= item:
                self.indices.insert(i+1,index)
                break


class PostingsList:

    def __init__(self):
        self.list = []
        self.documents_index = {}

    def add_posting(self, doc_id: int, index: int):
        pass
