from ddbb.DBManager import DBManager
from scraping import SourceManager
from view.HomeView import HomeView


class HomeController:
    def __init__(self, master_view, master_controller):
        self.view = HomeView(master_view)
        self.items = []
        self.parentView = master_view
        self.parentController = master_controller
        self.db_manager = DBManager()
        print()


    def show_view(self):
        self.view = HomeView(self.parentView)
        self.view.init_frame()
        self.view.btnSearch.config(command=self.on_search_request)
        if len(self.db_manager.get_sources()) == 0:
            self.db_manager.get_items("sources")
        self.view.update_src_items(self.db_manager.sources)
        self.get_news_items()

    def hide_view(self):
        self.view.destroy_view()

    def get_news_items(self):
        items = []
        if len(self.db_manager.sources) > 0:
            print()
            #items = SourceManager.get_data(self.db_manager.instance.sources[0])
        self.view.update_news_items(items)

    def on_search_request(self):
        print(self.view.searchInput)

    def on_toggle_source(self):
        print()
