"""
This is the starting script for a flask server app
page routes:
    '/' index, return index.html
    
api routes:
    '/api/wordcloud' return json, formatted wordcloud data structure

"""

from flask import Flask, request, Response
from analysis.fetch_news import fetch_news
from utils.firebase import firebaseAPI
from config import firebaseConfig, keywords, mapping
from news.news import NewsAPI
from news.handle import search_news
import json
import os
import random

# set the project root directory as the static folder, you can set others.
app = Flask(__name__,
            static_url_path='',
            static_folder='./frontend/build')
firebase = firebaseAPI(firebaseConfig)


@app.route('/api/wordcloud', methods=['get'])
def getWordCloud():
    """
    generate a wordcloud json and return to client
    """
    new_wordcloud = {'words': []}

    for i in range(0, 70):
        new_wordcloud['words'].append({
            'text': 'hello',
            'value': random.randrange(1, 100, 1)
        })

    for i in range(0, 70):
        new_wordcloud['words'].append({
            'text': 'world',
            'value': random.randrange(1, 100, 1)
        })

    print(json.dumps(new_wordcloud, indent=2))
    return json.dumps(new_wordcloud)


def trim_news(res):
    for res_ele in res:
        isValid = True
        for essential_key in ['description', 'title', 'url', 'urlToImage']:
            if essential_key not in res_ele:
                res.remove(res_ele)
                isValid = False
                break
        if not isValid:
            continue
        for extra_key in ['content', 'publishedAt', 'source', 'author']:
            if extra_key in res_ele:
                del res_ele[extra_key]
    return res


@app.route('/news_list', methods=["GET"])
def getNewsList():
    question = request.args.get("question")
    print("New Search: {0}".format(question))
    search_words = question.split(" ")
    feedback = []
    for search_word in search_words:
        for keyword in mapping.keys():
            if search_word.lower() in mapping[keyword]:
                news_list = fetch_news(firebase, start_time=[
                    0, 0, 0, 0, 0], keyword=keyword, entry="")
                print(news_list)
                if news_list != None:
                    feedback.extend(news_list)
    res = []
    [res.append(x) for x in feedback if x not in res]
    if res == []:
        newsapi = NewsAPI()
        for search_word in search_words:
            res.extend(search_news("us", None, search_word, newsapi))
    res = trim_news(res)
    print("Return data: {0}".format(res))
    return json.dumps(res)


@app.route('/')
def index():
    """
    default
    """
    return app.send_static_file('index.html')


if __name__ == "__main__":
    app.run(port=9000)
