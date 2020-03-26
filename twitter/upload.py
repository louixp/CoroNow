from utils.firebase import firebaseAPI
from config import firebaseConfig
import glob
import json
import pprint


def upload_dict(dictObj, api):
    for key in dictObj.keys():
        print(key)
        for time_arr in dictObj[key]:
            for time in time_arr.keys():
                print("--"+time)
                for keyword_arr in time_arr[time]:
                    for keyword in keyword_arr.keys():
                        print("----"+keyword)
                        for tweet in keyword_arr[keyword]:
                            print("-------"+str(tweet["id"]))
                            api.store_data(
                                key, tweet, [str(time), str(keyword), str(tweet["id"])])


def upload(firebase):
    data_list = []
    for dir in glob.glob('./data/[0-9]*-[0-9]*-[0-9]*-[0-9]*'):
        date = dir.split('/')[2]
        time_list = []
        for jsonfile in glob.glob("{0}/tweets_*".format(dir)):
            keyword = jsonfile.split('/')[3].replace(
                ".json", "").replace("tweets_", "")
            tweet_list = []
            db = open(jsonfile, "r", encoding='utf-8')
            print("Database opened for reading")
            for tweet_str in db:
                tweet = json.loads(tweet_str)
                tweet_list.append(tweet)
            tweet_col = {keyword: tweet_list}
            time_list.append(tweet_col)
        time_col = {date: time_list}
        data_list.append(time_col)
    data_col = {"tweets": data_list}
    upload_dict(data_col, firebase)
