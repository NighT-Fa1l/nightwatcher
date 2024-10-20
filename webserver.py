from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=5000)

# This function can be used to start the Flask server
def keep_alive():
    thread = threading.Thread(target=run)
    thread.start()
