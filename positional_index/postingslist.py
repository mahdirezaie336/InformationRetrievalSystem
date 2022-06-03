class Item:

    def __init__(self, doc_id: int):
        self.doc_id = doc_id
        self.indices = []

    def add_index(self, index):
        for i, item in enumerate(self.indices[::-1]):
            if index >= item:
                self.indices.insert(len(self.indices) - i, index)
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
                i += 1
                j += 1
            elif self.indices[i] > other.indices[j]:
                j += 1
            else:
                i += 1
        return new_item

    def __add__(self, other: int):
        new_item = Item(self.doc_id)
        for index in self.indices:
            new_item.indices.append(index + other)
        return new_item

    def __len__(self):
        return len(self.indices)


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

    def add_item(self, item: Item):
        self.documents_index[item.doc_id] = len(self.list)
        self.list.append(item)
        # TODO: Handle when the new item was exists before

    def __str__(self):
        return str(self.list)

    def __repr__(self):
        return str(self)

    def __and__(self, other: 'PostingsList'):
        new_postings_list = PostingsList()
        i, j = 0, 0
        while i < len(self.list) and j < len(other.list):
            if self.list[i].doc_id == other.list[j].doc_id:
                new_item = self.list[i] & other.list[j]
                new_item.doc_id = self.list[i].doc_id
                new_postings_list.add_item(new_item)
                i += 1
                j += 1
            elif self.list[i].doc_id > other.list[j].doc_id:
                j += 1
            else:
                i += 1
        return new_postings_list

    def __add__(self, other: int):
        new_postings_list = PostingsList()
        new_postings_list.documents_index = self.documents_index
        for item in self.list:
            new_postings_list.add_item(item + 1)
        return new_postings_list

    def __len__(self):
        return len(self.list)

    def get_term_frequency(self, doc_id):
        index = self.documents_index[doc_id]
        return self.list[index]

    def get_document_frequency(self):
        return len(self)
