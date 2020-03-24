import sys
import json
from news import NewsAPI
from utils import calculate_time, save_date

def search(country, category, keyword):
    print("Search for data country: {0}, keyword: {1}, category: {2}".format(country, keyword, category))
    newsapi = NewsAPI()
    if calculate_time() >= 60:
        newsapi.update_sources()
        save_date()
    return json.dumps(newsapi.headlines(keyword=keyword, country=country, category=category))

def main():
    country = input("Country: [gb|au|us|ca|it|ie|in|is]: ")
    category = input("Category: [general|business|technology|sports|entertainment|health|science]: ")
    keyword = input("Keyword: ")
    print(search(country, category, keyword))

if __name__ == '__main__':
    main()
    