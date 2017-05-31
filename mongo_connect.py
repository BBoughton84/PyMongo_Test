from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import json
import requests
from pprint import pprint
import os
import datetime
from datetime import timedelta
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

@app.route('/insert/<barcode>')
def inserting(barcode):

    food = mongo.db.foods
    itemToIncrease = food.find_one({'barcode':barcode})
    if(itemToIncrease):
        print("There is something in here, lets add one to the QTY")
        itemToIncrease['quantity'] += 1
        food.save(itemToIncrease)
        output = {'brand_name': itemToIncrease['brand_name'], 'item_name': itemToIncrease['item_name'], 'quantity':itemToIncrease['quantity']}
        return jsonify({'result': output})

    else:
        source = requests.get('https://api.nutritionix.com/v1_1/item?upc=%s&appId=84f8ed7f&appKey=d476c24cdcdf18749e8ca0e5b9bce022' % barcode)
        brandName = source.json()["brand_name"]
        itemName = source.json()["item_name"]
        serveSize = source.json()["nf_serving_size_qty"]
        servePerCont = source.json()["nf_servings_per_container"]
        units = source.json()["nf_serving_size_unit"]

        food.insert({'brand_name':brandName, 'item_name':itemName, 'size':serveSize, 'servings_per_container':servePerCont, 'units':units, 'barcode':barcode, 'quantity':1})
        return "item added " + brandName + " " + itemName


@app.route('/manadd')
def add():
    user = mongo.db.users
    user.insert({'name' : 'John', 'language' : 'JavaScript'})
    user.insert({'name' : 'Matt', 'language' : 'Java'})
    user.insert({'name' : 'Joe', 'language' : 'Python'})
    user.insert({'name' : 'Kyle', 'language' : 'Ruby'})
    user.insert({'name' : 'Dan', 'language' : 'C'})
    return 'All users added!'

@app.route('/insertdate', methods=['GET'])
def insertdate():
    user = mongo.db.newdates
    user.insert({'name': 'Bob', 'type': 'golden', 'date_added':[], 'date_removed':[]})
    user.insert({'name': 'Kait', 'type': 'lab', 'date_added':[], 'date_removed':[]})
    return 'dogs added'

@app.route('/persondateadd/<name>')
def persondateadd(name):
    user = mongo.db.newdates
    userFound = user.find_one({'name': name})
    userFound['date_added'].append(datetime.datetime.now())
    user.save(userFound)
    return "date added"

@app.route('/persondateremove/<name>')
def persondateremove(name):
    user = mongo.db.newdates
    userFound = user.find_one({'name': name})
    userFound['date_removed'].append(datetime.datetime.now())
    user.save(userFound)
    print(userFound['date_removed'][1])
    return "date added"

@app.route('/returndates')
def returndates():
    user = mongo.db.newdates
    output = []
    for user in user.find():
        diff=[]
        for i in range(len(user['date_removed'])):
            print(i)
            time1 = user['date_added'][i]
            time2 = user['date_removed'][i]
            delta = time2-time1
            diff.append(str(delta).split('.', 2)[0])
        output.append({'name':user['name'], 'type':user['type'], 'date_added':user['date_added'], 'date_removed':user['date_removed'], 'date_difference':diff})

        # time1 = i['date_added'][0]
        # time2 = i['date_removed'][0]
        # delta = time2-time1
        # print(str(delta).split('.', 2)[0])
    return jsonify({'result': output})

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

@app.route('/showfoods')
def show_foods():
    item = mongo.db.foods
    output = []
    for food in item.find():
        output.append({
        'brand_name':food['brand_name'],
        'item_name':food['item_name'],
        'size':food['size'],
        'servings_per_container':food['servings_per_container'],
        'units':food['units'],
        'quantity':food['quantity']
        })

    return jsonify({'result':output})

@app.route('/throwaway/<barcode>')
def trash(barcode):
    food = mongo.db.foods
    itemToTrash = food.find_one({'barcode':barcode})
    if(itemToTrash):
        if(itemToTrash['quantity']==1):
            print("There is ONE in here")
            itemToTrash['quantity'] = 0
            food.save(itemToTrash)
            return "item removed"
        elif(itemToTrash['quantity'] > 1):
            print("There is more than one, less decrease by one")
            itemToTrash['quantity'] -= 1
            food.save(itemToTrash)
            return "decreased the quantity by one"
        else:
            print("this item is at zero quantity")
            return "this item is at zero quantity"
    else:
        print("Item does not exist")
        return "This item does not exist"


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
