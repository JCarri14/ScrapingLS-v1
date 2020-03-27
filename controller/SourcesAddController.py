from ddbb.DBManager import DBManager
from view.SourcesAddView import SourceAddView
from model.SourceFilter import SourceFilter
from model.ScrapingSource import ScrapingSource

class SourcesAddController:
    def __init__(self, master_view, master_controller):
        self.parentView = master_view
        self.parentController = master_controller
        self.view = SourceAddView(master_view)
        self.source = ScrapingSource(None, None)
        self.db_manager = DBManager()

    def show_view(self):
        self.view = SourceAddView(self.parentView)
        self.view.init_view()
        self.view.btnAccept.config(command=self.on_accept_request)
        self.view.btnDecline.config(command=self.on_decline_request)
        self.view.btnAddFilter.config(command=self.on_add_filter_request)

    def on_accept_request(self):
        self.source.name = self.view.source_name.get("1.0", "end-1c")
        self.source.url = self.view.source_url.get("1.0", "end-1c")
        self.db_manager.insert_item("sources", self.source)
        self.parentController.on_hide_add_view_from_add()

    def on_decline_request(self):
        self.parentController.on_hide_add_view_from_cancel()

    def on_add_filter_request(self):
        result = self.view.filterResult.get()
        name = self.view.filterReference.get("1.0", "end-1c")
        value = self.view.filterValue.get("1.0", "end-1c")
        self.source.filters.append(SourceFilter(result, name, value))
        #self.view.add_filter_item(SourceFilter(result, name, value))
        self.view.update_filters_list(self.source.filters)

    def on_update_request(self):
        self.source.name = self.view.source_name.get("1.0", "end-1c")
        self.source.url = self.view.source_url.get("1.0", "end-1c")
        self.db_manager.update_item("sources", self.source)
        self.parentController.on_hide_add_view_from_add()

    def on_update_view(self, source):
        self.show_view()
        self.view.btnAccept.config(command=self.on_update_request)
        self.source.filters = source.filters
        self.view.update_view(source.name, source.url, source.filters)




