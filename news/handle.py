import sys
import json
from .news import NewsAPI
from utils.utils import calculate_time, save_date


def check_update(api):
    if calculate_time() >= 60:
        api.update_sources()
        save_date()
        return True
    else:
        return False


def search_news(country, category, keyword, api):
    print("Search for data country: {0}, keyword: {1}, category: {2}".format(
        country, keyword, category))
    return api.headlines(keyword=keyword, country=country, category=category)
