from newsapi.newsapi_client import NewsApiClient
from config import apikey, database
import json


class NewsAPI:
    def __init__(self):
        self.api = NewsApiClient(api_key=apikey)

    def headlines(self, keyword=None, sources=None, country=None, category=None,  lang="en"):
        source_str = None
        if sources != None:
            source_str = ""
            for i in range(len(sources)-1):
                source_str += sources[i] + ","
            source_str += sources[len(sources)-1]
        top_headlines = self.api.get_top_headlines(q=keyword,
                                                   sources=source_str,
                                                   category=category,
                                                   language=lang,
                                                   country=country)
        return top_headlines['articles']

    def update_sources(self):
        sources = self.api.get_sources()['sources']
        db = open(database, 'w')
        print("Database opened for writing")
        json.dump(sources, db)
        db.close()
        print("Database closed for writing")

    def get_sources(self):
        print("Preparing news...")
        db = open(database, "r")
        print("Database opened for reading")
        sources = json.load(db)
        db.close()
        print("Database closed for reading")
        return sources
