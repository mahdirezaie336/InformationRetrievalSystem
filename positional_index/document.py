class Document:

    def __init__(self, _id):
        self.__id = _id
        self.__content = ''
        self.__tokens = []

    def __hash__(self):
        return hash(self.__id)

    def __eq__(self, other):
        return other.__id == self.__id

    def __str__(self):
        return 'ID: ' + str(self.__id)