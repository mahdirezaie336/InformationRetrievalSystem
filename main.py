from positional_index import PositionalIndex
import json


def load_json_file(address) -> dict:
    with open(address) as json_file:
        docs = json.load(json_file)
    return docs


def preprocess(docs):
    # Doing the preprocesses
    print('Started preprocessing ...')
    for doc_id in docs:
        text = docs[doc_id]['content']
        stemmed_tokens = PositionalIndex.preprocess(text)
        docs[doc_id]['tokens'] = stemmed_tokens
    print('Finished preprocessing')
    return docs


def create_index(docs) -> PositionalIndex:
    index = PositionalIndex()
    for doc_id in docs:
        index.add_from_dict(doc_id, docs[doc_id])
    return index


def main():
    # Load JSON file
    docs = load_json_file('./IR_data_news_12k.json')

    # Do preprocesses
    docs = preprocess(docs)

    # Creating index
    index = create_index(docs)
    print(index)


if __name__ == '__main__':
    main()
