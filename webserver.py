from flask import Flask
from threading import Threading

app = Flask('')
@app.route('/')
def home():
    return "discord bot ok"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(terget=run)
    t.start()
