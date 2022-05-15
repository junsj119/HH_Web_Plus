from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import certifi
import requests

app = Flask(__name__)
ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.uhugw.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta_plus_week2


@app.route('/')
def main():
    # DB에서 저장된 단어 찾아서 HTML에 나타내기
    msg = request.args.get("msg")
    words = list(db.words.find({}, {"_id":False}))
    return render_template("index.html", words=words, msg=msg)


@app.route('/detail/<keyword>')
def detail(keyword):
    status_receieve = request.args.get("status_give")
    # API에서 단어 뜻 찾아서 결과 보내기
    r = requests.get(f"https://owlbot.info/api/v4/dictionary/{keyword}", headers={"Authorization": "Token 9f94b684399f9e595d58001cae76ce3d64c40f28"})
    if r.status_code != 200:
        return redirect(url_for("main", msg="단어가 이상해유"))
        #return redirect("/") 두 개 다 같은 뜻

    result = r.json()
    return render_template("detail.html", word=keyword, result=result, status=status_receieve)


@app.route('/api/save_word', methods=['POST'])
def save_word():
    # 단어 저장하기
    word_receieve = request.form["word_give"]
    definition_receive = request.form["definition_give"]

    doc = {
        'word':word_receieve,
        'definition':definition_receive
    }
    db.words.insert_one(doc)

    return jsonify({'result': 'success', 'msg': f'단어 {word_receieve}저장'})


@app.route('/api/delete_word', methods=['POST'])
def delete_word():
    # 단어 삭제하기
    word_receieve = request.form['word_give']
    db.words.delete_one({'word':word_receieve})
    return jsonify({'result': 'success', 'msg': f'단어 {word_receieve}삭제'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)