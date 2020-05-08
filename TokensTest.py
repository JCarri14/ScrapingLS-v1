from tokenizer.MessageTokenizer import MssgTokenizer


if __name__ == '__main__':
    tokenizer = MssgTokenizer('spanish')
    #tokenizer.find_syn('perro', 'spa')
    #tokenizer.getCorrectTerm('habitacions')
    print(tokenizer.termFilter('arboles'))
    #tokenizer.ownStemmer('trabajando')

