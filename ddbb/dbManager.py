from ddbb.DBFactory import DBFactory
from ddbb.MongoFactory import MongoFactory
from ddbb.Neo4jFactory import Neo4jFactory

class DBManager:
    __instance = None

    class __Manager:
        def __init__(self):
            self.mongoFactory = None
            self.neo4jFactory = None
            self.current_factory = None
            self.sources = []
            self.news = []
            self.bagOfWords = []
            self.aux_old_item = None

    instance = None

    def __init__(self):
        if not DBManager.instance:
            DBManager.instance = DBManager.__Manager()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def get_sources(self):
        return self.instance.sources

    def insert_item(self, location, item):
        self.instance.current_factory.set_item_location(location)
        self.instance.current_factory.insert_item(item)

    def update_item(self, location, item):
        self.instance.current_factory.set_item_location(location)
        self.instance.current_factory.set_aux_old_item(self.instance.aux_old_item)
        self.instance.current_factory.update_item(item)

    def delete_item(self, location, item):
        self.instance.current_factory.set_item_location(location)
        self.instance.current_factory.delete_item(item)

    def get_items(self, location):
        self.instance.current_factory.set_item_location(location)
        if location == "sources":
            self.instance.sources = self.instance.current_factory.get_items()
        else:
            if location == "news":
                self.instance.news = self.instance.current_factory.get_items()
            else:
                if location == "bagOfWords":
                    self.instance.bagOfWords = self.instance.current_factory.get_items()

    def get_item_by_name(self, location, name):
        self.instance.current_factory.set_item_location(location)
        self.instance.current_factory.get_item_by_name(name)

    def setFactorySource(self, name):
        if name == "Mongo":
            if self.instance.mongoFactory is None:
                self.instance.mongoFactory = MongoFactory()
            self.instance.current_factory = self.mongoFactory
        else:
            if name == "Neo4j":
                if self.instance.neo4jFactory is None:
                    self.instance.neo4jFactory = Neo4jFactory(None, None, None)
                self.instance.current_factory = self.neo4jFactory
