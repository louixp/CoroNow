"""
This is the starting script for a flask server app
"""

from flask import Flask, request, Response
import json
import os

static_path = os.path.abspath(os.path.dirname(__file__))

# set the project root directory as the static folder, you can set others.
app = Flask(__name__,
            static_url_path='',
            static_folder='../frontend/build')


@app.route('/')
def index():
    """
    default
    """
    return app.send_static_file('index.html')


if __name__ == "__main__":
    app.run(port=3459)
