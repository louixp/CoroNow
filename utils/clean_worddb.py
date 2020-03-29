import json
from config import wordquerydb


def clean(year, month, date, hour):
    f = open(wordquerydb, "r")
    ele = json.load(f)
    f.close()
    del ele["{0}-{1}-{2}-{3}".format(year, month, date, hour)]
    f = open(wordquerydb, "w")
    json.dump(ele, f)
    f.close()
