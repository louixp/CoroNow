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
from config import firebaseConfig, keywords, mapping, wordquerydb
from news.news import NewsAPI
from news.handle import search_news
from utils.utils import format_date, calculate_diff_hour, change_date
from analysis.count_word import word_count
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
    worddb = open(wordquerydb, "r")
    print("Word data opened for reading")
    wordcloud_data = json.load(worddb)
    worddb.close()
    print("Word data closed for reading")
    date_str = format_date(4)
    exact_date = [int(it) for it in date_str.split("-")]
    exact_date.append(0)
    word_list = []
    if date_str not in wordcloud_data.keys():
        word_list, frequency = word_count(firebase)
        if(word_list[0]["word"] == ""):
            data_keys = wordcloud_data.keys()
            sorted_keys = sorted(data_keys, key=lambda x: int(x.split(
                "-")[1])*30*24 + int(x.split("-")[2])*24 + int(x.split("-")[3]), reverse=True)
            word_list = wordcloud_data[sorted_keys[0]]
        wordcloud_data[date_str] = word_list
        worddb = open(wordquerydb, "w")
        print("Word data opened for writing")
        json.dump(wordcloud_data, worddb)
        worddb.close()
        print("Word data closed for writing")
    else:
        word_list = wordcloud_data[date_str]
    new_wordcloud = {'words': []}
    for word in word_list:
        new_wordcloud["words"].append({
            'text': word["word"].upper(),
            'value': int((word["frequency"]+50)/2)
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


@app.route('/trend', methods=["GET"])
def getWordTrend():
    word = request.args.get("word").lower()
    print("New Word: {0}".format(word))
    worddb = open(wordquerydb, "r")
    print("Word data opened for reading")
    wordcloud_data = json.load(worddb)
    worddb.close()
    print("Word data closed for reading")
    date_str = format_date(4)
    word_date = {}
    word_date["word"] = word
    word_date["frequency"] = []
    for key in wordcloud_data.keys():
        old_date_arr = [int(it) for it in key.split("-")]
        new_date_arr = [int(it) for it in date_str.split("-")]
        if calculate_diff_hour(old_date_arr, new_date_arr) <= 24:
            for ele in wordcloud_data[key]:
                if ele["word"] == word:
                    word_date["frequency"].append({
                        "date": old_date_arr,
                        "value": ele["frequency"]
                    })
    print("Send: {0}", json.dumps(word_date))
    return json.dumps(word_date)


@app.route('/')
def index():
    """
    default
    """
    return app.send_static_file('index.html')


if __name__ == "__main__":
    app.run(port=9000)
