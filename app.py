# Copyright (c) 2020 Sharvil Kekre skekre98
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from flask import Flask, jsonify, redirect, render_template, request

from data.text_data import non_nba, unsure
from modules.analysis import isNBA
from modules.query import Query
from modules.scraper import get_playoff_bracket
from modules.transformer import create_html_bracket

app = Flask(__name__)


"""
Function to handle routing to home page.

Parameters
----------
n/a

Returns
-------
HTML file
    Rendering of HTML template for home page.
"""


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/home")
def home2():
    return render_template("home.html")


"""
Function to handle routing to chatbox page.

Parameters
----------
n/a

Returns
-------
HTML file
    Rendering of HTML template for chatbox page
"""


@app.route("/chat")
def chat():
    return render_template("chat.html")


"""
Function to render blogs page.

Parameters
----------
n/a

Returns
-------
HTML file
    Rendering of HTML template for blog page
"""


@app.route("/blog")
def blog():
    return render_template("blogs.html")


"""
Function to handle routing to authors page.

Parameters
----------
n/a

Returns
-------
HTML file
    Rendering of HTML template for authors page
"""


@app.route("/authors")
def authors():
    return render_template("authors.html")


"""
Function to handle routing to predictions page.

Parameters
----------
n/a

Returns
-------
HTML file
    Rendering of HTML template for predictions page
"""


@app.route("/predictions")
def predictions():
    bracket = get_playoff_bracket()
    bracket = create_html_bracket(bracket)
    return render_template("predictions.html", bracket=bracket)


"""
Function to download requested blog for user.

Parameters
----------
n/a

Returns
-------
HTML file
    Rendering of HTML template for blog page.
"""


@app.route("/download/<string:id>", methods=["GET", "POST"])
def download(id):
    if id is None:
        self.Error(400)
    try:
        blog_map = {
            "1": "https://drive.google.com/uc?export=download&id=13FmzW70fMMfTwrypxzJRG-J6woty8ePz",  # Dog pic
            "2": "https://drive.google.com/uc?export=download&id=13FmzW70fMMfTwrypxzJRG-J6woty8ePz",  # Dog pic
            "3": "https://drive.google.com/uc?export=download&id=13FmzW70fMMfTwrypxzJRG-J6woty8ePz",  # Dog pic
        }
        return redirect(blog_map[id])
    except Exception as e:
        self.log.exception(e)
        self.Error(400)


"""
Function to handle POST request from user
with embedded message. The message is then
passed to the chatbot and the response is returned
to user.

Parameters
----------
request : json
    The POST request sent from user sending a message

Returns
-------
Bot response : json
    The chatbot response to user message
"""


@app.route("/bot-msg", methods=["POST"])
def get_bot_response():
    usr_msg = request.form["msg"]
    handler = Query(usr_msg)
    response = handler.process()
    return jsonify(response)


if __name__ == "__main__":
    app.run()
