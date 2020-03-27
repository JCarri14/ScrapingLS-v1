from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from model.ScrapingSource import ScrapingSource
from model.SourceFilter import SourceFilter
from model.SourceItem import SourceItem


def get_data(source: ScrapingSource):
    try:
        html = urlopen(source.url)
    except HTTPError as e:
        print(e)
    except URLError as e:
        print(e)
    else:
        res = BeautifulSoup(html.read(), "html.parser")
        newsContent = None
        title_filter = None
        thumbnail_filter = None

        for f in source.filters:
            if f.expected_result == "item-container":
                newsContent = res.findAll("div", {f.name: f.value})

        for f in source.filters:
            if f.expected_result == "title":
                title_filter = f
            else:
                if f.expected_result == "thumbnail":
                    thumbnail_filter = f

        data = []
        for item in newsContent:
            title = item.find("div", {title_filter.name: title_filter.value}).getText()
            thumbnail = item.find("img", {thumbnail_filter.name: thumbnail_filter.value})
            data.append(SourceItem(title, thumbnail, None, None, None, None))

        print(data)
        print(len(data))
        return data

