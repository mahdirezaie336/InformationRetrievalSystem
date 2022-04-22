from parsivar import Normalizer, Tokenizer, FindStems
from stopwordsiso import stopwords
from positional_index.index import PositionalIndex
import json
import pandas as pd


def load_json_file(address) -> dict:
    with open(address) as json_file:
        docs = json.load(json_file)
    return docs


def preprocess(docs):
    # Defining the preprocessors
    normalizer = Normalizer()
    tokenizer = Tokenizer()
    stemmer = FindStems()
    stop_words = stopwords('fa')

    # Doing the preprocesses
    print('Started preprocessing ...')
    for doc_id in docs:
        text = docs[doc_id]['content']
        normalized_text = normalizer.normalize(text)            # Normalization
        tokens = tokenizer.tokenize_words(normalized_text)      # Tokenization
        nonstop_tokens = []                                     # Handling stop words
        for token in tokens:
            if token not in stop_words:
                nonstop_tokens.append(token)
        stemmed_tokens = pd.Series(nonstop_tokens).apply(stemmer.convert_to_stem).values        # Getting stems
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
