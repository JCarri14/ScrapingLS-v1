class ScrapingSource:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.filters = []

    def set_name(self, name):
        self.name = name

    def set_url(self, url):
        self.url = url

    def add_filter(self, filter_item):
        self.filters.append(filter_item)
