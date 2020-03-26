from utils.firebase import firebaseAPI
from config import firebaseConfig
from .handle import search_news, check_update
from .news import NewsAPI
from utils.utils import format_date
from config import keywords
import json


def news_init(base, api):
    date = format_date()
    for keyword in keywords:
        news_list = search_news('us', None, keyword, api)
        for news in news_list:
            base.store_data(
                "news", news, [date, keyword, news["publishedAt"]])
            print("==== News uploaded ====")
    return
