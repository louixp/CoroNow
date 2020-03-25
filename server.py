"""
This is the starting script for a flask server app
page routes:
    '/' index, return index.html
    
api routes:
    '/api/wordcloud' return json, formatted wordcloud data structure

"""

from flask import Flask, request, Response
import json
import os

# set the project root directory as the static folder, you can set others.
app = Flask(__name__,
            static_url_path='',
            static_folder='frontend/build')


@app.route('/api/wordcloud', methods=['get'])
def getWordCloud():
    """
    generate a wordcloud json and return to client
    """
    new_wordcloud = {'hello': 10, 'yes': 9, 'foo': 8, 'bar': 7}
    print(json.dumps(new_wordcloud))
    return json.dumps(new_wordcloud)


@app.route('/')
def index():
    """
    default
    """
    return app.send_static_file('index.html')


if __name__ == "__main__":
    app.run(port=3000)
