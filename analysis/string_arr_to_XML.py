from .fetch_tweets import fetch_tweets
from lxml import etree
from utils.utils import check_date

# Usage
# pip install lxml
# firebase = firebaseAPI(firebaseConfig)
# print(convert_to_XML(firebase, [start_time ...]))


def convert_to_XML(firebase, start_time=[], end_time=check_date(), keyword="Coronavirus", entry="tweet"):
    strarr = fetch_tweets(firebase, start_time, end_time, keyword, entry)
    root = etree.Element('sentences')
    _id = 0
    for _str in strarr:
        child = etree.Element('sentence')
        text = etree.Element('text')
        text.text = _str
        child.append(text)
        child.set("id", str(_id))
        root.append(child)
        _id += 1
    s = etree.tostring(root, pretty_print=True).decode()
    return s
