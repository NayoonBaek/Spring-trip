from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.bqbsmxx.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/spring", methods=["POST"])
def spring_post():
    img_receive = request.form['img_give']
    title_receive = request.form['title_give']
    food_receive = request.form['food_give']

    num = 1

    spring_list = list(db.springs.find({}, {'_id': False}))

    try:
        count = spring_list[-1]['num']
    except:
        count = 0

    while num <= count:
        num += count

    doc = {
        'num': num,
        'img': img_receive,
        'title': title_receive,

        'food': food_receive,
    }
    db.springs.insert_one(doc)
    return jsonify({'msg': '기록 완료!'})

@app.route("/spring", methods=["GET"])
def spring_get():
    spring_list = list(db.springs.find({}, {'_id': False}))
    return jsonify({'springs': spring_list})


@app.route("/save/edit", methods=["POST"])
def edit_post():
    num_receive = request.form['num_give']
    img_receive = request.form['img_give']
    title_receive = request.form['title_give']
    food_receive = request.form['food_give']

    db.springs.update_one({'num': int(num_receive)}, {'$set': {'img': img_receive, 'title': title_receive, 'food': food_receive}})
    return jsonify({'msg': '수정 완료!'})

@app.route("/delete", methods=["POST"])
def delete_post():
    num_receive = request.form['num_give']
    db.springs.delete_one({'num': int(num_receive)})
    return jsonify({'msg': '삭제 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)