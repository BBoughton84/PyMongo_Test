from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import json

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'test_db'
app.config['MONGO_URI'] = 'mongodb://jake:test123@ds153501.mlab.com:53501/test_db'

mongo = PyMongo(app)

@app.route('/manadd')
def add():
    user = mongo.db.users
    user.insert({'name' : 'John', 'language' : 'JavaScript'})
    user.insert({'name' : 'Matt', 'language' : 'Java'})
    user.insert({'name' : 'Joe', 'language' : 'Python'})
    user.insert({'name' : 'Kyle', 'language' : 'Ruby'})
    user.insert({'name' : 'Dan', 'language' : 'C'})
    return 'All users added!'

@app.route('/add', methods=['POST'])
def sendadd():
    user = mongo.db.users

    # name = json.loads(request.data['name'])
    # language = json.loads(request.data['language'])

    name = request.json['name']
    language = request.json['language']

    user_id = user.insert({'name': name, 'language': language})
    new_user = user.find_one({'_id': user_id})

    output = {'name': new_user['name'], 'language':new_user['language']}

    return jsonify({'result': output})

@app.route('/newtable', methods=['GET'])
def addmore():
    user = mongo.db.dogs
    user.insert({'name': 'jake', 'type': 'golden'})
    user.insert({'name': 'jax', 'type': 'lab'})
    return 'dogs added'

@app.route('/find')
def find():
    user = mongo.db.users
    kyle = user.find_one({'name':'Kyle'})
    # return 'this is ' + kyle['name'] + ' and he speaks ' + kyle['language']
    return jsonify({'result': kyle['name']})

# @app.route('/addnew', methods=['POST'])

@app.route('/update', methods=['POST'])
def update():
    user = mongo.db.users

    findName = request.json['oldname']
    changeName = request.json['newname']

    oldPerson = user.find_one({'name': findName})
    print(changeName)
    # oldPerson['name'] = changeName
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
    # return output


@app.route('/remove')
def remove():
    user = mongo.db.users
    userToRemove = framework.user.find_one({'name' : 'Bill'})
    user.remove(userToRemove)
    return 'user removed'

if __name__ == '__main__':
    app.run(debug=True)
