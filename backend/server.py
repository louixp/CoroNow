"""
This is the top-level starting script for a flask server app
"""

from flask import Flask, request
import json
import devices

# set the project root directory as the static folder, you can set others.
app = Flask(__name__,
            static_url_path='',
            static_folder='../frontend/build')


@app.route('/api/markEvent', methods=['POST'])
def markEvent():
    """
    mark the next coming line from 
    """
    pass


if __name__ == "__main__":
    app.run()
