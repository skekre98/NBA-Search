from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__)

chatbot = ChatBot("SHAq")
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/test")
def test():
    return render_template("author.html")

@app.route("/bot-msg", methods=['POST'])
def get_bot_response():
    usr_msg = request.form['msg']
    bot_msg = str(chatbot.get_response(usr_msg))
    return jsonify(bot_msg)

if __name__ == "__main__":
    app.run()