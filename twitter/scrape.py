import twint
import datetime

def get_tweets(keyword, limit):
    c = twint.Config()
    c.Search = keyword
    c.Lang = "en"
    c.Limit = limit
    c.Store_object = True
    c.Store_json = True
    c.Output = f"scraped_tweets_{datetime.date.today()}_{datetime.datetime.now().time()}.json"
    twint.run.Search(c)

if __name__ == "__main__":
    get_tweets("covid-19", 100)