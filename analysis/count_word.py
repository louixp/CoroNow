from .fetch_tweets import fetch_tweets
from utils.utils import check_date
from config import keywords
from twitter.scrape import clean_tweet


def word_count(firebase, start_time=[], end_time=check_date()):
    tweets = []
    for keyword in keywords:
        tweets.extend(fetch_tweets(firebase, start_time, end_time, keyword))
    sum_tweet = ""
    for tweet in tweets:
        sum_tweet += tweet
    sum_tweet = clean_tweet(sum_tweet)
    sum_words = sum_tweet.split(" ")
    red_sum_words = []
    [red_sum_words.append(x) for x in sum_words if x not in red_sum_words]
    freq_list = []
    for word in red_sum_words:
        freq_list.append({
            "word": word,
            "frequency": sum_words.count(word)
        })
    sorted_freq_list = sorted(
        freq_list, key=lambda k: k['frequency'], reverse=True)
    return (sorted_freq_list, sorted_freq_list[0]['frequency'])
