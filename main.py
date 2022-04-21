from parsivar import Normalizer, Tokenizer, FindStems
from positional_index import PositionalIndex
import json


def preprocess():
    pass


def main():
    # with open('./IR_data_news_12k.json') as json_file:
    #     body = json.load(json_file)
    #     print(body['0'])
    text = 'سلام. امروز سال ۱۴۰۱ می باشد.'
    normalizer = Normalizer()
    tokenizer = Tokenizer()
    stemmer = FindStems()
    text = normalizer.normalize(text)
    print(text)
    print(tokenizer.tokenize_words(text))
    print(stemmer.convert_to_stem('آمدم'))


if __name__ == '__main__':
    main()
