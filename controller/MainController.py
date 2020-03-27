from ddbb.DBManager import DBManager
from view.MainView import MainView
from controller.HomeController import HomeController
from controller.SourcesController import SourceController
from utils.Constants import *


class Controller:
    def __init__(self, root):
        self.db_manager = DBManager()
        self.db_manager.setFactorySource("Mongo")
        self.mainView = MainView(root)
        self.mainView.init_view()
        self.config_upper_panel_btns()
        self.init_controllers()
        self.homeController.show_view()

    def config_upper_panel_btns(self):
        self.mainView.btnHome.config(command=self.on_home_request)
        self.mainView.btnSrc.config(command=self.on_sources_request)
        self.mainView.btnStats.config(command=self.on_stats_request)

    def init_controllers(self):
        self.homeController = HomeController(self.mainView, self)
        self.srcController = SourceController(self.mainView, self)
        self.currentController = self.homeController

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