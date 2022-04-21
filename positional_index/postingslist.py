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

    list: list[Item]

    def __init__(self):
        self.list = []
        self.documents_index = {}           # Keeping index of documents in postings list to have fast access

    def add_posting(self, doc_id: int, index: int):
        if doc_id not in self.documents_index:
            self.documents_index[doc_id] = len(self.list)
            new_item = Item(Document(doc_id))
            new_item.add_index(index)
            for item in self.list
            self.list.append(new_item)
        else:
            doc_index = self.documents_index[doc_id]
            self.list[doc_index].add_index(index)
