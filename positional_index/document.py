class Document:

    def __init__(self, _id):
        self.id = _id
        self.content = ''
        self.tokens = []
        self.title = ''
        self.date = ''
        self.url = ''
        self.category = ''
        self.tags = ''

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return other.id == self.id

    def __str__(self):
        return 'ID: ' + str(self.id)

    def __gt__(self, other):
        return self.id > other.id

    def __lt__(self, other):
        return self.id < other.id

    def __ge__(self, other):
        return self.id >= other.id

    def __le__(self, other):
        return self.id <= other.id

    def to_dict(self, attrs=None):
        if attrs is None:
            return {'title': self.title,
                    'content': self.content,
                    'category': self.category,
                    'date': self.date,
                    'url': self.url,
                    'tag': self.tags}
        d = {}
        for item in attrs:
            d[item] = getattr(self, item)
        return d

    @staticmethod
    def parse_from_dict(_id: str, d: dict) -> 'Document':
        doc = Document(int(_id))
        doc.title = d['title']
        doc.content = d['content']
        doc.tags = d['tags']
        doc.date = d['date']
        doc.url = d['url']
        doc.category = d['category']
        if 'tokens' in d:
            doc.tokens = d['tokens']
        return doc
