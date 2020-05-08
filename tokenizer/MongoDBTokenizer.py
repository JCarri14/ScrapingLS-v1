import pymongo
from nltk.data import LazyLoader
from nltk.tokenize import TreebankWordTokenizer
from nltk.util import AbstractLazySequence, LazyMap, LazyConcatenation


class MongoDBTokenizer(AbstractLazySequence):
    def __init__(self, host='localhost', port=27017, db='db_scraping',
                 collection='media', field='noticia'):
        self.conn = pymongo.MongoClient(host, port)
        self.collection = self.conn[db][collection]
        self.field = field

    def __len__(self):
        return self.collection.count()

    def iterate_from(self, start):
        f = lambda d: d.get(self.field, '')
        return iter(LazyMap(f, self.collection.find(skip=start)))


class MongoDBCorpusReader(object):
    def __init__(self, word_tokenizer=TreebankWordTokenizer(),
                 sent_tokenizer=LazyLoader('tokenizers/punkt/spanish.pickle'),**kwargs):
        self._seq = MongoDBTokenizer(**kwargs)
        self._word_tokenize = word_tokenizer.tokenize
        self._sent_tokenize = sent_tokenizer.tokenize

    def text(self):
        return self._seq

    def words(self):
        return LazyConcatenation(LazyMap(self._word_tokenize,
                                         self.text()))
    def sents(self):
        return LazyConcatenation(LazyMap(self._sent_tokenize,
                                         self.text()))