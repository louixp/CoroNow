from utils.utils import check_date, change_date, compare_date, calculate_time, save_date
from config import news_datefile, newsquerydb
import pickle

# start_time: [year, month, day, hour, minute] (int array)
# end_time: [year, month, day, hour, minute] (int array)


def fetch_news(firebase, start_time=[], end_time=check_date(), keyword="Coronavirus", entry="content"):
    return_list = []
    if start_time == []:
        start_time = change_date(end_time, hour=-1)
    if calculate_time(news_datefile) >= 60:
        news_data = firebase.retrieve_data("news")
        _output = open(newsquerydb, "wb")
        pickle.dump(news_data, _output, -1)
        _output.close()
        print("Query storage updated")
        save_date(news_datefile)
    else:
        _input = open(newsquerydb, "rb")
        news_data = pickle.load(_input)
        _input.close()
        print("Query storage loaded")
    for news in news_data.each():
        key = news.key()
        data_time = key.split("-")
        data_time = [int(ele) for ele in data_time]
        if compare_date(data_time, start_time) == "Greater" and compare_date(data_time, end_time) == "Less":
            print("News fetched by NEWSAPI at {0}".format(key))
            data = news.val()
            try:
                current_news = data[keyword]
                current_news_arr = []
                for time_key in current_news.keys():
                    try:
                        if entry != "":
                            current_news_arr.append(
                                current_news[time_key][entry])
                        else:
                            current_news_arr.append(current_news[time_key])
                    except:
                        pass
                return_list.extend(current_news_arr)
            except KeyError:
                pass
    return return_list
