class Item:

    def __init__(self, doc_id: int):
        self.doc_id = doc_id
        self.indices = []

    def add_index(self, index):
        for i, item in enumerate(self.indices[::-1]):
            if index >= item:
                self.indices.insert(i + 1, index)
                return
        self.indices.append(index)

    def __str__(self):
        return str(self.doc_id) + ': ' + str(self.indices)

    def __repr__(self):
        return str(self)

    def __and__(self, other: 'Item'):
        new_item = Item(0)
        i, j = 0, 0
        while i < len(self.indices) and j < len(other.indices):
            if self.indices[i] == other.indices[j]:
                new_item.indices.append(self.indices[i])
            elif self.indices[i] > other.indices[j]:
                j += 1
            else:
                i += 1


class PostingsList:

    list: list[Item]

    def __init__(self):
        self.list = []
        self.documents_index = {}           # Keeping index of documents in postings list to have fast access

    def add_posting(self, doc_id: int, index: int):
        if doc_id not in self.documents_index:
            self.documents_index[doc_id] = len(self.list)
            new_item = Item(doc_id)
            new_item.add_index(index)
            # TODO: Handle adding in center of list
            self.list.append(new_item)
        else:
            doc_index = self.documents_index[doc_id]
            self.list[doc_index].add_index(index)

    def __str__(self):
        return str(self.list)

    def __repr__(self):
        return str(self)

    def __and__(self, other: 'PostingsList'):
        new_list = []
        i, j = 0, 0
        while i < len(self.list) and j < len(other.list):
            if self.list[i].doc_id == other.list[j].doc_id:
                new_list.append()
