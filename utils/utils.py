import datetime
import json
from config import datefile


def check_date():
    now = datetime.datetime.now()
    return [now.year, now.month, now.day, now.hour, now.minute]


def save_date():
    date = check_date()
    dateObj = {
        "year": date[0],
        "month": date[1],
        "day": date[2],
        "hour": date[3],
        "minute": date[4]
    }
    f = open(datefile, 'w')
    json.dump(dateObj, f)
    f.close()


def format_date():
    date = check_date()
    return "{0}-{1}-{2}-{3}-{4}".format(date[0], date[1], date[2], date[3], date[4])


def load_date():
    f = open(datefile, 'r')
    dateObj = json.load(f)
    f.close()
    return [dateObj["year"], dateObj["month"], dateObj["day"], dateObj["hour"], dateObj["minute"]]


def calculate_time():
    newdate = check_date()
    olddate = load_date()
    diff = ((newdate[0] - olddate[0]) * 365 + (newdate[1] - olddate[1]) * 30 + newdate[2] -
            olddate[2]) * 24 * 60 + (newdate[3] - olddate[3]) * 60 + newdate[4] - olddate[4]
    return diff
