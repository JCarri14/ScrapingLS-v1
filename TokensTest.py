from tokenizer.MessageTokenizer import MssgTokenizer
from tokenizer.CorpusReader import CorpusReader
from tokenizer.ConllReader import ConllReader
from tokenizer.MongoDBTokenizer import MongoDBCorpusReader
import nltk.data


if __name__ == '__main__':
    tokenizer = MssgTokenizer('spanish')
    #tokenizer.find_syn('perro', 'spa')
    #tokenizer.getCorrectTerm('habitacions')
    #print(tokenizer.termFilter('arboles'))
    #tokenizer.ownStemmer('trabajando')
    #tokenizer.readCorpusList()
    #tokenizer.readCatgCorpus()
    """path = nltk.data.find('corpora/cookbook')
    pattern = r'news_.*\.txt'
    reader = CorpusReader(path, pattern, cat_file='bryan_adams.txt')
    for sent in reader.chunked_words():
        print(sent)
    
    path = nltk.data.find('corpora/cookbook')
    pattern = r'news_.*\.txt'
    reader = ConllReader(path, pattern, ('NP','VP','PP') , cat_file='bryan_adams.txt')
    for sent in reader.chunked_sents():
        print(sent)
    """
    reader = MongoDBCorpusReader(db='db_scraping', collection='media',
                                 field='noticia')
    print(reader.sents())
