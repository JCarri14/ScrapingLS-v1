from scraping.TwitterManager import TwitterManager
from view.MainView import *
from controller.MainController import Controller


if __name__ == '__main__':

    twitter = TwitterManager().instance
    #twitter.read_tweets_from_source('lavanguardia')
    twitter.start_stream_from_source('lavanguardia')

    print("Hola")
    root = Tk()
    root.withdraw()
    app = Controller(root)
    root.mainloop()
