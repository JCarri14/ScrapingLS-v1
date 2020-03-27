from pymongo import MongoClient

from ddbb.DBFactory import DBFactory
from model.ScrapingSource import ScrapingSource
from model.SourceFilter import SourceFilter


class MongoFactory(DBFactory):

    def __init__(self):
        self.client = MongoClient(port=27017)
        self.db = self.client["db_scraping"]
        self.collection = self.db["sources"]
        self.collection_name = "sources"
        self.items = []
        self.aux_old_item = None

    def close(self):
        self.client.close()

    def set_item_location(self, location):
        self.collection_name = location
        self.collection = self.db[location]

    def insert_item(self, source):
        src = self.toSourceDBModel(source)
        self.collection.insert_one(src)

    def update_item(self, source):
        self.delete_item(self.aux_old_item)
        self.insert_item(source)
        #src = self.getMappedModel(source)
        #myquery = {"name": self.aux_old_source.name, "url": self.aux_old_source.url}
        #newvalues = {"$set": {"name": source.name, "url": source.url, "filters": source.filters}}
        #self.collection.update_one(myquery, newvalues

    def delete_item(self, source):
        src = self.toSourceDBModel(source)
        query = {"name": src['name'], "url": src['url']}
        self.collection.delete_one(query)

    def get_items(self):
        print("Sending Request...")
        self.items = []
        #self.collection = self.db["sources"]
        for item in self.collection.find():
            size = len(item["filters"])
            item_new = ScrapingSource(item["name"], item["url"])
            if size > 0:
                item_new.filters = self.toPythonFiltersModel(item["filters"])
            self.items.append(item_new)
        print("Request received!")
        return self.items

    def get_item_by_name(self, name):
        query = {"name": name}
        res = self.collection.find_one(query)

    def toSourceDBModel(self, source):
        filters = self.toSourceDBFilters(source)
        src = {
            "name": source.name,
            "url": source.url,
            "filters": filters
        }
        return src

    def toSourceDBFilters(self, source):
        filters = []
        for item in source.filters:
            f = {
                "expected_result": item.expected_result,
                "name": item.name,
                "value": item.value
            }
            filters.append(f)
        return filters

    def toPythonFiltersModel(self, filters):
        newList = []
        for filter in filters:
            newFilter = SourceFilter(filter["expected_result"],
                                     filter["name"],
                                     filter["value"])
            newList.append(newFilter)
        return newList

    def set_aux_old_item(self, item):
        self.aux_old_item = item





