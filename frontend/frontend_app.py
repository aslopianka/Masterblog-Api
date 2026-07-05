"""
This module contains a simple Flask application for the frontend.
"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    """
    Renders the home page of the frontend application.
    """
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
