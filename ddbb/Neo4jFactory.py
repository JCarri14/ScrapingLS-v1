from neo4j import GraphDatabase
from ddbb.DBFactory import DBFactory


class Neo4jFactory(DBFactory):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
        self.sources = []
        self.news = []
        self.bagOfWords = []
        self.aux_old_source = None

    def close(self):
        self._driver.close()

    def set_item_location(self, location):
        print("To be implemented...")

    def insert_item(self, item): pass

    def update_item(self, item): pass

    def delete_item(self, item): pass

    def get_items(self): pass

    def get_item_by_name(self, name): pass