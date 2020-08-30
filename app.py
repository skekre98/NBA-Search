import os
from modules.analysis import isNBA
from modules.scraper import get_playoff_bracket
from modules.transformer import create_html_bracket
from modules.query import Query
from data.text_data import unsure, non_nba
from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__)

os.system('python3 -m spacy download en_core_web_sm')
chatbot = ChatBot("SHAq")
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")

"""
Function to handle routing to home page.

Parameters
----------
n/a

Returns
-------
HTML file
    Rendering of HTML template for home page
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
    flag = isNBA(usr_msg)
    if flag == -1:
        return jsonify(non_nba)
    elif flag == 0:
        return jsonify(unsure)
    else:
        handler = Query(usr_msg)
        response = handler.process()
        return jsonify(response)

if __name__ == "__main__":
    app.run()