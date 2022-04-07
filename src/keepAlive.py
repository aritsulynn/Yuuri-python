from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Hey! I'm a discord bot not a website!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keepAlive():
    t = Thread(target=run)
    t.start()
