from firebase import firebaseAPI
from config import firebaseConfig
from handle import search_news
import json

def main():
    firebase = firebaseAPI(firebaseConfig)
    news_list = search_news('us', None, 'corona')
    if news_list != None:
        for news in news_list:
            firebase.store_data("news", news, str(news["publishedAt"]))
            print("News uploaded")
    else:
        print("No more uploads needed")
        return
                

if __name__ == "__main__":
    main()