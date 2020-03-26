from firebase import firebaseAPI
from config import firebaseConfig
from handle import search_news, check_update
from news import NewsAPI
from utils import format_date
from config import keywords
import json

def main():
    firebase = firebaseAPI(firebaseConfig)
    newsapi = NewsAPI()
    date = format_date()
    if check_update(newsapi):
        for keyword in keywords:
            news_list = search_news('us', None, keyword, newsapi)
            for news in news_list:
                firebase.store_data("news", news, [date, keyword, news["publishedAt"]])
                print("News uploaded")
    else:
        print("No more uploads needed")
        return

if __name__ == "__main__":
    main()