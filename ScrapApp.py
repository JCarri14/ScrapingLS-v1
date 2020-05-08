from scraping.TwitterManager import TwitterManager
from tokenizer.MessageTokenizer import MssgTokenizer
from view.MainView import *
from controller.MainController import Controller


if __name__ == '__main__':

    twitter = TwitterManager().instance
    #twitter.read_tweets_from_source('lavanguardia')
    twitter.start_stream_from_source('lavanguardia')
    tokenizer = MssgTokenizer('spanish')
    print(tokenizer.find_syn('perro'))

    """print("Hola")
    root = Tk()
    root.withdraw()
    app = Controller(root)
    root.mainloop()"""
