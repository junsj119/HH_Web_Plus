from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import certifi

app = Flask(__name__)


ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.uhugw.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.sparta03


@app.route('/')
def main():
    return render_template("index.html")


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)