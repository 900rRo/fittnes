import os
from threading import Thread
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Service is running!"

def run():
    app.run(host='0.0.0.0', port=80)

def keep_alive():
    thread = Thread(target=run)
    thread.start()

if __name__ == '__main__':
    keep_alive()
