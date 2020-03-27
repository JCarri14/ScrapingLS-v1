from ddbb.DBManager import DBManager
from view.SourcesView import SourcesView
from controller.SourcesAddController import SourcesAddController


class SourceController:
    def __init__(self, master_view, master_controller):
        self.parentController = master_controller
        self.parentView = master_view
        self.view = SourcesView(master_view)
        self.db_manager = DBManager()
        self.addController = SourcesAddController(self.view.data_container, self)

    def show_view(self):
        self.view = SourcesView(self.parentView)
        self.view.init_view()
        self.view.btnAdd.config(command=self.on_add_view_request)
        if len(self.db_manager.instance.sources) == 0:
            self.db_manager.get_items("sources")

        self.view.update_src_items(self.db_manager.instance.sources)
        self.view.set_list_listener(self.on_update_source_request, self.on_delete_source_request)

    def hide_view(self):
        self.view.destroy()

    def on_update_source_request(self, index):
        self.db_manager.instance.aux_old_item = self.db_manager.instance.sources[index]
        self.on_add_view_request()
        self.addController.on_update_view(self.db_manager.instance.aux_old_item)

    def on_delete_source_request(self, index):
        self.db_manager.delete_item(self.db_manager.sources[index])
        self.on_hide_add_view_from_add()

    def on_add_view_request(self):
        self.view.hide_data_container()
        self.addController = SourcesAddController(self.view.aux_container, self)
        self.addController.show_view()

    def on_hide_add_view_from_add(self):
        self.db_manager.instance.sources = []
        self.show_view()

    def on_hide_add_view_from_cancel(self):
        self.show_view()


