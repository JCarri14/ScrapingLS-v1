from tkinter import *
from tkinter.font import Font
from view.HomeView import HomeView
from view.SourcesView import SourcesView
from utils.Constants import *


class MainView(Toplevel):
    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.protocol('WM_DELETE_WINDOW', self.master.destroy)
        self.homeView = HomeView(self)
        self.srcView = SourcesView(self)
        self.currentView = self.homeView
        self.btnHome = None
        self.btnSrc = None
        self.btnStats = None
        self.viewContainer = None

    def init_view(self):
        self.geometry(SCREEN_SIZE)
        self.title(APP_TITLE)
        self.init_top_nav()
        self.init_content_view()

    def init_top_nav(self):
        nav = Frame(self, bg=COLOR_DARK)
        nav.place(relx=0, rely=0, relwidth=1, relheight=0.1)

        btnContainer = Frame(nav, bg=COLOR_DARK)
        btnContainer.place(relx=0.05, rely=0, relwidth=0.9, relheight=1)

        boldFont = Font(weight="bold")
        self.btnHome = Button(btnContainer, text=HOME_LABEL, font=boldFont, bg=COLOR_WHITE, fg=COLOR_DARK)
        self.btnHome.place(relx=0, rely=0.3, relwidth=0.2, relheight=0.5)
        self.btnHome.config(command=self.get_home_view)

        self.btnSrc = Button(btnContainer, text=SRC_LABEL, font=boldFont, bg=COLOR_WHITE, fg=COLOR_DARK)
        self.btnSrc.place(relx=0.21, rely=0.3, relwidth=0.2, relheight=0.5)
        self.btnSrc.config(command=self.get_src_view)

        self.btnStats = Button(btnContainer, text=STATS_LABEL, font=boldFont, bg=COLOR_WHITE, fg=COLOR_DARK)
        self.btnStats.place(relx=0.42, rely=0.3, relwidth=0.2, relheight=0.5)
        self.btnStats.config(command=self.get_stats_view)

    def init_content_view(self):
        self.homeView.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

    def get_home_view(self):
        if self.currentView != self.homeView:
            self.currentView.destroy()
            self.homeView = HomeView(self)
            self.homeView.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
            self.currentView = self.homeView

    def get_src_view(self):
        if self.currentView != self.srcView:
            self.currentView.destroy()
            self.srcView = SourcesView(self)
            self.srcView.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
            self.currentView = self.srcView
        return True

    def get_stats_view(self):
        return True


