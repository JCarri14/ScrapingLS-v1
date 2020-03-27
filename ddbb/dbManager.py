from pymongo import MongoClient

from model.ScrapingSource import ScrapingSource
from model.SourceFilter import SourceFilter


class Database:

    def __init__(self):
        self.client = MongoClient(port=27017)
        self.db = self.client["db_scraping"]
        self.collection = self.db["sources"]
        self.sources = []
        self.aux_old_source = None

    def addSource(self, source):
        src = self.getMappedModel(source)
        self.collection.insert_one(src)

    def getMappedModel(self, source):
        filters = []
        for item in source.filters:
            f = {
                "expected_result": item.expected_result,
                "name": item.name,
                "value": item.value
            }
            filters.append(f)
        src = {
            "name": source.name,
            "url": source.url,
            "filters": filters
        }
        return src

    def updateSource(self,source):
        self.deleteSource(self.aux_old_source)
        self.addSource(source)
        #src = self.getMappedModel(source)
        #myquery = {"name": self.aux_old_source.name, "url": self.aux_old_source.url}
        #newvalues = {"$set": {"name": source.name, "url": source.url, "filters": source.filters}}
        #self.collection.update_one(myquery, newvalues)

    def set_aux_old_source(self, source):
        self.aux_old_source = source

    def requestSources(self):
        print("Sending Request...")
        for item in self.collection.find():
            print(item)
            source = ScrapingSource(item["name"],
                                    item["url"])
            filter_list = []
            for filter in item["filters"]:
                newFilter = SourceFilter(filter["expected_result"],
                                         filter["name"],
                                         filter["value"])
                source.add_filter(newFilter)
            self.sources.append(source)
        print("Request received...")

    def deleteSource(self, source):
        src = self.getMappedModel(source)
        query = {"name": src['name'], "url": src['url']}
        self.collection.delete_one(query)

