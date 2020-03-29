from utils.utils import check_date, change_date, compare_date, calculate_time, save_date
from config import tweet_datefile, tweetquerydb
import pickle

# start_time: [year, month, day, hour, minute] (int array)
# end_time: [year, month, day, hour, minute] (int array)


def fetch_tweets(firebase, start_time=[], end_time=check_date(), keyword="Coronavirus", entry="tweet"):
    return_list = []
    if start_time == []:
        start_time = change_date(end_time, hour=-1)
    if calculate_time(tweet_datefile) >= 60:
        tweet_data = firebase.retrieve_data("tweets")
        _output = open(tweetquerydb, "wb")
        pickle.dump(tweet_data, _output, -1)
        _output.close()
        print("Query storage updated")
        save_date(tweet_datefile)
    else:
        _input = open(tweetquerydb, "rb")
        tweet_data = pickle.load(_input)
        _input.close()
        print("Query storage loaded")
    for tweet_col in tweet_data.each():
        key = tweet_col.key()
        data_time = key.split("-")
        data_time = [int(ele) for ele in data_time]
        if compare_date(data_time, start_time, 4) == "Greater" and compare_date(data_time, end_time, 4) != "Greater":
            print("Tweet fetched by TWINT at {0}".format(key))
            data = tweet_col.val()
            current_tweets = data[keyword]
            current_tweets_arr = []
            for id_key in current_tweets.keys():
                try:
                    current_tweets_arr.append(current_tweets[id_key][entry])
                except:
                    pass
            return_list.extend(current_tweets_arr)
    return return_list
