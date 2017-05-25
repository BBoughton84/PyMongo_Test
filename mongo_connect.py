from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'test_db'
app.config['MONGO_URI'] = 'mongodb://jake:test123@ds153501.mlab.com:53501/test_db'

mongo = PyMongo(app)

@app.route('/add')
def add():
    user = mongo.db.users
    user.insert({'name' : 'Bill'})
    return 'added user!'

if __name__ == '__main__':
    app.run(debug=True)
