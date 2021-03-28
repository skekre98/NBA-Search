from modules.analysis import isNBA
from modules.scraper import *
from modules.transformer import create_html_bracket
from modules.query import Query
from data.text_data import unsure, non_nba
from flask import Flask, render_template, request, jsonify, redirect
import numpy as np


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
@app.route("/download/<string:id>", methods=['GET', 'POST'])
def download(id):
    if id is None:
        self.Error(400)
    try:
        blog_map ={
            "1" : "https://drive.google.com/uc?export=download&id=13FmzW70fMMfTwrypxzJRG-J6woty8ePz", # Dog pic
            "2" : "https://drive.google.com/uc?export=download&id=13FmzW70fMMfTwrypxzJRG-J6woty8ePz", # Dog pic
            "3" : "https://drive.google.com/uc?export=download&id=13FmzW70fMMfTwrypxzJRG-J6woty8ePz"  # Dog pic
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
@app.route("/bot-msg", methods=['POST'])
def get_bot_response():
    usr_msg = request.form['msg']
    handler = Query(usr_msg)
    response = handler.process()
    return jsonify(response)

@app.route("/v1/player/<string:name>/stats/<string:stat>")
def player(name, stat):
    stats = get_total_stat(name, stat)
    print(stats)
    return jsonify(player_name=name,
                    stats=stats)

@app.route("/v1/player/fullstat/<string:name>/")
def full_stat(name):
    name = get_target_name(name)
    json = []
    for key, value in dict.items(total_stat_map):
        full_stats = get_total_stat(name, key)
        json.append(full_stats)

    json_array = np.array(json)
    return jsonify(player_name = name, stats = json)

if __name__ == "__main__":
    app.run()