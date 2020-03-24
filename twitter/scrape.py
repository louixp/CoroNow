import twint
import datetime
from collections import Counter

# keywords provided by https://arxiv.org/abs/2003.07372
keywords = {"Coronavirus", "Koronavirus", "Corona", "CDC", "Wuhancoronavirus", "Wuhanlockdown", "Ncov", 
            "Wuhan", "N95", "Kungflu", "Epidemic", "Outbreak", "Sinophobia", "China", "Covid-19 ", 
            "Corona virus", "Covid", "Covid19", "Sars-cov-2", "COVID–19", "COVD", "Pandemic"}

def get_tweets(keyword, limit):
    c = twint.Config()
    c.Search = keyword
    c.Lang = "en"
    c.Limit = limit
    c.Store_object = True
    c.Store_json = True
    c.Output = f"scraped_tweets_{datetime.date.today()}_{datetime.datetime.now().time()}.json"
    twint.run.Search(c)

def clean_tweet(tweet):
    pass

def word_freq():
    pass
    
def hashtag_freq():
    return Counter([h for t in twint.output.tweets_list for h in t.hashtags])

if __name__ == "__main__":
    get_tweets("covid-19", 100)