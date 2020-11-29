import flask
from flask import request, jsonify
from flask_restful import Api, Resource
from resources.user import Users, User
from resources.accounts import Accounts,Account
import pymysql

app = flask.Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)
api.add_resource(Users, '/users')
api.add_resource(User, '/user/<id>')
api.add_resource(Accounts, '/bank-accounts')
api.add_resource(Account, '/bank-account/<id>')
#api.add_resource(Users, '/users/<id>') #如果要用動態

@app.route('/', methods=['GET'])
def home():
    return "<h3>Bello<h3>"

@app.route('/account/<account_number>/deposit', methods=['POST'])
def deposit(account_number):
    db, cursor, account = get_account(account_number)
    money = request.values['money']
    balance = account['balnce'] + int(money)
    sql = """
    Update flask_demo.Accounts set balance = {}
    where account_number = '{}'
    """.format(balance, account_number)
    cursor.execute(sql)
    db.commit()
    db.close()
    response = {
        'result': True
    }
    return jsonify(response)

def get_account(account_number):
    
    db = pymysql.connect('192.168.56.101',
                    'Tzujung','admin123', 'flask_demo')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = """
        Select * From flask_demo.Accounts
        where account_number = '{}'
        """.format(account_number)
    cursor.execute(sql)
    return db, cursor, cursor.fetchone()
# 
if __name__ == '__main__':
    app.run(port=5000)