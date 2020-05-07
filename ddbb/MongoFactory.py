from pymongo import MongoClient

from ddbb.DBFactory import DBFactory
from model.ScrapingSource import ScrapingSource
from model.SourceFilter import SourceFilter

#COLLECTIONS:   [ SOURCES ] ; [ MEDIA ]
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
        if self.collection_name == "sources":
            src = self.toSourceDBModel(source)
            self.collection.insert_one(src)
        else:
            if self.collection_name == "media":
                res = None
                if 'comment' not in source:
                    if 'original_media_name' in source:
                        res = self.get_item_by_name(source['original_media_name'])
                    else:
                        res = self.get_item_by_name(source['media_name'])
                    if res is not None:
                        found = False
                        for t in res['tweets']:
                            if t["text"] == source["tweet"]["text"]:
                                t["retweets"] += 1
                                found = True
                        if not found:
                            res["tweets"].append(source["tweet"])

                        self.update_item(res)
                    else:
                        src = self.toMediaDBModel(source)
                        self.collection.insert_one(src)
                else:
                    res = self.get_item_by_name(source['media_name'])
                    if res is not None:
                        for t in res['tweets']:
                            if t['tweet_id'] == source['tweet']['tweet_id']:
                                if t['comments']: # list is not empty
                                    print()
                                else:
                                    print()
                    print()

    def update_item(self, source):
        if self.collection_name == "sources":
            self.delete_item(self.aux_old_item)
            self.insert_item(source)
        else:
            if self.collection_name == "media":
                myquery = {"media_name": source['media_name']}
                newvalues = {"$set": {"tweets": source['tweets']}}
                self.collection.update_one(myquery, newvalues)
        #src = self.getMappedModel(source)


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
        res = None
        if self.collection_name == "sources":
            query = {"name": name}
            res = self.collection.find_one(query)
        else:
            if self.collection_name == "media":
                query = {"media_name": name}
                res = self.collection.find_one(query)
        return res

    def toMediaNewDBModel(self, item):
        return item

    def toMediaDBModel(self, item):
        filteredItem = {}
        if 'original_media_name' in item:
            filteredItem['media_name'] = item['original_media_name']
        else:
            filteredItem['media_name'] = item['media_name']
        filteredItem['tweets'] = []
        filteredItem["tweets"].append(item["tweet"])
        return filteredItem

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
            newFilter = SourceFilter(filter["expected_result"], None,
                                     filter["name"],
                                     filter["value"])
            newList.append(newFilter)
        return newList

    def set_aux_old_item(self, item):
        self.aux_old_item = item





