from .fetch_tweets import fetch_tweets
from lxml import etree
from config import keywords, xml_data
from utils.utils import check_date, change_date

# Usage
# pip install lxml
# firebase = firebaseAPI(firebaseConfig)
# print(convert_to_XML(firebase, time))


def convert_to_XML(firebase, time):
    edtime = change_date(time, minute=30)
    strarr = []
    for keyword in keywords:
        strarr.extend(fetch_tweets(firebase, end_time=edtime, keyword=keyword))
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
    s = etree.tostring(root, pretty_print=True)
    f = open(xml_data, "wb+")
    f.write(s)
    f.close()
    s = s.decode()
    return s
