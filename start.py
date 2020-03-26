from news.init import news_init
from twitter.scrape import twitter_init
from utils.firebase import firebaseAPI
from utils.utils import calculate_time, format_date, save_date
from news.news import NewsAPI
from config import firebaseConfig
import time


# source [0: newsapi, 1: twint, 2: both] | mode [0: fetch, 1: upload, 2: both]
def main(source=2, mode=2):
    firebase = firebaseAPI(firebaseConfig)
    newsapi = NewsAPI()
    while(True):
        if calculate_time() >= 60:
            if source == 2 or source == 0:
                print("\n== Newsapi started ==\n")
                news_init(firebase, newsapi)
                print("\n== Newsapi finished ==\n")
            if source == 2 or source == 1:
                print("\n== Twint started ==\n")
                twitter_init(firebase, mode)
                print("\n== Twint finished ==\n")
            save_date()
        else:
            date = format_date()
            print("\n== Waiting at {0} ==\n".format(date))
        time.sleep(60)


if __name__ == "__main__":
    main(2, 2)