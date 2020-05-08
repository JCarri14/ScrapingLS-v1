from nltk.tokenize import RegexpTokenizer, PunktSentenceTokenizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer, LancasterStemmer, \
    RegexpStemmer, SnowballStemmer
from nltk.stem import WordNetLemmatizer
from tokenizer.Replacer import Replacer



class MssgTokenizer:

    __language = None

    def __init__(self, lang):
        self.__language = lang

    def sentence_to_tokens(term, sentence):
        tokenizer = RegexpTokenizer("[\w']+")
        words = tokenizer.tokenize(sentence)
        print(words)
        return words

    def find_syn(self, term, lang):
        syns = wordnet.synsets('casa', lang=lang)
        for s in syns:
            print(s.lemma_names('spa'))

    def remove_stop_words(self, sentence):
        stops_words = set(stopwords.words(self.__language))
        res = [word for word in sentence if word not in stops_words]
        return res

    def check_similarity_with(self, term, master_term):
        cd = wordnet

    def stemAction(self, term):
        #stemmer = PorterStemmer()
        stemmer = LancasterStemmer()
        print(stemmer.stem(term))

    def regexStemmer(self, term):
        v_sufixos = ['ando', 'endo', 's', 'é']
        expr = 's$|es$'
        stemmer = RegexpStemmer(expr)
        return stemmer.stem(term)

    def getCorrectTerm(self, term):
        replacer = Replacer('es_ANY', 1)
        res = replacer.replace(term)
        return res

    def termFilter(self, term):
        syns = wordnet.synsets(term, lang='spa')
        if len(syns) == 0:
            checkedTerm = self.getCorrectTerm(term)

            if checkedTerm == term:
                res = self.regexStemmer(term)
                syns = wordnet.synsets(res, lang='spa')

                if len(syns) == 0:
                    checkedTerm = self.getCorrectTerm(res)

                    if checkedTerm == res:
                        stemmer = SnowballStemmer('spanish')
                        res = (stemmer.stem(term))
                        aux_term = res
                        sufixes = ['ar', 'er', 'ir']

                        for s in sufixes:
                            aux_term = aux_term + s
                            syns = wordnet.synsets(aux_term, lang='spa')

                            if len(syns) > 0:
                                return aux_term
                            else:
                                aux_term = res
                        return term
                    else:
                        return checkedTerm
                else:
                    return res
            else:
                return checkedTerm
        else:
            return term

    def lemmatizeTerm(self, term):
        lematizer = WordNetLemmatizer()
        print(lematizer.lemmatize(term, pos="n"))

    def readCorpusList(self):
        print()




