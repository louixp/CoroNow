import twint
import datetime
from collections import Counter
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import ssl

# keywords provided by https://arxiv.org/abs/2003.07372
keywords = {"Coronavirus", "Koronavirus", "Corona", "CDC", "Wuhancoronavirus", "Wuhanlockdown", "Ncov", 
            "Wuhan", "N95", "Kungflu", "Epidemic", "Outbreak", "Sinophobia", "China", "Covid-19 ", 
            "Corona virus", "Covid", "Covid19", "Sars-cov-2", "COVID–19", "COVD", "Pandemic"}

def download_nltk_resources():
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

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
    cleaned_tweet = ""
    # remove urls
    no_url = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet, flags=re.MULTILINE)
    # tokenize sentences
    sentences = sent_tokenize(no_url)
    for s in sentences:
        # lowercase sentences
        lowered = s.lower()
        # tokenize word
        words = word_tokenize(lowered)
        # remove punctuation and stop words
        cleaned = [w for w in words if re.search('[a-zA-Z]', w) and not w in stopwords.words('english')]
        # lemmatize words
        wl = WordNetLemmatizer()
        lemmas = [wl.lemmatize(w) for w in cleaned]
        # join cleaned tweet
        cleaned_tweet += ' '.join(lemmas)
        cleaned_tweet += ' '
    return cleaned_tweet

def word_freq():
    pass
    
def hashtag_freq():
    return Counter([h for t in twint.output.tweets_list for h in t.hashtags])

if __name__ == "__main__":
    download_nltk_resources()
    get_tweets("covid-19", 100)