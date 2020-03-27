from ddbb.dbManager import Database
from view.MainView import MainView
from controller.HomeController import HomeController
from controller.SourcesController import SourceController
from utils.Constants import *

class Controller:
    def __init__(self, root):
        self.db_manager = Database()
        self.mainView = MainView(root)
        self.mainView.init_view()
        self.homeController = HomeController(self.mainView, self, self.db_manager)
        self.srcController = SourceController(self.mainView, self, self.db_manager)
        self.mainView.btnHome.config(command=self.on_home_request)
        self.mainView.btnSrc.config(command=self.on_sources_request)
        self.mainView.btnStats.config(command=self.on_stats_request)
        self.mainFrame = root
        self.currentController = self.homeController
        self.homeController.show_view()

    def on_home_request(self):
        if self.currentController != self.homeController:
            self.currentController.hide_view()
            self.currentController = self.homeController
            self.homeController.show_view()

    def on_sources_request(self):
        if self.currentController != self.srcController:
            self.currentController.hide_view()
            self.currentController = self.srcController
            self.srcController.show_view()

    def on_stats_request(self):
        return True