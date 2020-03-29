import datetime
import json
from config import datefile


def check_date():
    now = datetime.datetime.now()
    return [now.year, now.month, now.day, now.hour, now.minute]


def change_date(date, day=0, hour=0, minute=0):
    old_date = datetime.datetime(date[0], date[1], date[2], date[3], date[4])
    new_date = old_date + \
        datetime.timedelta(days=day, hours=hour, minutes=minute)
    return [new_date.year, new_date.month, new_date.day, new_date.hour, new_date.minute]


def compare_date(fdate, sdate, length=5):
    for ind in range(length):
        if int(fdate[ind]) < int(sdate[ind]):
            return "Less"
        elif int(fdate[ind]) > int(sdate[ind]):
            return "Greater"
    return "Equal"


def save_date(_file=datefile):
    date = check_date()
    dateObj = {
        "year": date[0],
        "month": date[1],
        "day": date[2],
        "hour": date[3],
        "minute": date[4]
    }
    f = open(_file, 'w')
    json.dump(dateObj, f)
    f.close()


def format_date(entry_len=5):
    date = check_date()
    datestr = ""
    for i in range(entry_len-1):
        datestr += (str(date[i]) + "-")
    datestr += (str(date[entry_len-1]))
    return datestr


def load_date(_file=datefile):
    f = open(_file, 'r')
    dateObj = json.load(f)
    f.close()
    return [dateObj["year"], dateObj["month"], dateObj["day"], dateObj["hour"], dateObj["minute"]]


def calculate_time(_file=datefile):
    newdate = check_date()
    olddate = load_date(_file)
    diff = ((newdate[0] - olddate[0]) * 365 + (newdate[1] - olddate[1]) * 30 + newdate[2] -
            olddate[2]) * 24 * 60 + (newdate[3] - olddate[3]) * 60 + newdate[4] - olddate[4]
    return diff


def calculate_diff_hour(olddate, newdate):
    diff = ((newdate[0] - olddate[0]) * 365 + (newdate[1] - olddate[1]) * 30 + newdate[2] -
            olddate[2]) * 24 + (newdate[3] - olddate[3])
    return diff
