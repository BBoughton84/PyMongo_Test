from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import json
import requests
from pprint import pprint
import os
# import urllib

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'test_db'
app.config['MONGO_URI'] = 'mongodb://jake:test123@ds153501.mlab.com:53501/test_db'

port = int(os.environ.get('PORT', 5000))

mongo = PyMongo(app)

@app.route('/testingAPI/<barcode>')
def getBackData(barcode):
    source = requests.get('https://api.nutritionix.com/v1_1/item?upc=%s&appId=84f8ed7f&appKey=d476c24cdcdf18749e8ca0e5b9bce022' % barcode)

    pprint(source.json()["brand_name"])

    return jsonify({'result':source.json()})

@app.route('/manadd')
def add():
    user = mongo.db.users
    user.insert({'name' : 'John', 'language' : 'JavaScript'})
    user.insert({'name' : 'Matt', 'language' : 'Java'})
    user.insert({'name' : 'Joe', 'language' : 'Python'})
    user.insert({'name' : 'Kyle', 'language' : 'Ruby'})
    user.insert({'name' : 'Dan', 'language' : 'C'})
    return 'All users added!'

@app.route('/newtable', methods=['GET'])
def addmore():
    user = mongo.db.dogs
    user.insert({'name': 'jake', 'type': 'golden'})
    user.insert({'name': 'jax', 'type': 'lab'})
    return 'dogs added'

@app.route('/add', methods=['POST'])
def sendadd():
    user = mongo.db.users

    # name = json.loads(request.data['name']) //string
    # language = json.loads(request.data['language']) //string

    name = request.json['name']
    language = request.json['language']

    user_id = user.insert({'name': name, 'language': language})
    new_user = user.find_one({'_id': user_id})

    output = {'name': new_user['name'], 'language':new_user['language']}

    return jsonify({'result': output})


@app.route('/find/<name>')
def find(name):
    user = mongo.db.users
    findUser = user.find_one({'name':name})
    return jsonify({'result': {'name':findUser['name'], 'language':findUser['language']}})

@app.route('/update', methods=['POST'])
def update():
    user = mongo.db.users

    findName = request.json['oldname']
    changeName = request.json['newname']

    oldPerson = user.find_one({'name': findName})
    oldPerson['name'] = changeName
    user.save(oldPerson)
    output = {'name': oldPerson['name'], 'language': oldPerson['language']}
    return jsonify({'result': output})

@app.route('/framework', methods=['GET'])
def get_all():
    user = mongo.db.users
    output = []
    for item in user.find():
        output.append({'name': item['name'], 'language': item['language']})

    return jsonify({'result': output})


@app.route('/remove/<name>')
def remove(name):
    user = mongo.db.users
    userToRemove = user.find_one({'name' : name})
    user.remove(userToRemove)
    return 'user removed'

if __name__ == '__main__':
    # app.run(debug=True)
    app.debug = True
    app.run(host='0.0.0.0', port=port)
