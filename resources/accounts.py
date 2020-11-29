from flask_restful import Resource, reqparse
from flask import jsonify
import pymysql


parser = reqparse.RequestParser()
parser.add_argument('balance')
parser.add_argument('account_number')

# 整筆資料
class Accounts(Resource):
    def db_init(self):
        db = pymysql.connect('192.168.56.101',
                        'Tzujung','admin123', 'flask_demo')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    def get(self):
        db = pymysql.connect('192.168.56.101',
                'Tzujung','admin123', 'flask_demo')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = """Select * From flask_demo.Accounts where deleted = False"""
        cursor.execute(sql)
        accounts = cursor.fetchall()
        db.close()
        response = {
            'data' : accounts
        }
        return jsonify(response)

    def post(self):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        account = {
        'balance' : arg['balance'],
        'account_number' : arg['account_number']
        }
        sql = """
            Insert into flask_demo.Accounts
            (balance, account_number)
            values('{}','{}')
        """.format(account['balance'],account['account_number'])
        result = cursor.execute(sql)
        db.commit()
        db.close()
        response = {
            'result': True
        }
        return jsonify(response)


# 單筆資料
class Account(Resource):
    def db_init(self):
        db = pymysql.connect('192.168.56.101',
                        'Tzujung','admin123', 'flask_demo')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    def get(self, id):
        db, cursor = self.db_init()
        sql = """Select * From flask_demo.Accounts
            where id = '{}' and deleted = False
        """.format(id)
        cursor.execute(sql)
        account = cursor.fetchone()
        db.close()
        response = {
        'data': account
    }
        return jsonify(response)
    #更改資料
    def patch(self,id): 
        db, cursor = self.db_init()
        arg = parser.parse_args()
        account = {
        'balance' : arg['balance'],
        'account_number' : arg['account_number']
        }
        query = []
        for key, value in account.items():
            if value != None:
                query.append(key + ' =' + " '{}' ".format(value))
        query = ",".join(query)
        sql = """ Update flask_demo.Accounts Set {} where id = "{}"
        """.format(query, id)
        result = cursor.execute(sql)
        db.commit()
        db.close()
        response = {
            'result': True
        }
        return jsonify(response)
    #刪除
    def delete(self, id): 
        db, cursor = self.db_init()
        sql = """Delete From flask_demo.Accounts where id = '{}'
        """.format(id)
        cursor.execute(sql)
        db.commit()
        db.close()
        response = {
            'result': True
        }
        return jsonify(response)
    #軟刪除
    def delete(self, id):
        db, cursor = self.db_init()
        sql = """Update flask_demo.Accounts Set deleted = True where id = '{}'
        """.format(id)
        cursor.execute(sql)
        db.commit()
        db.close()
        response = {
            'result': True
        }
        return jsonify(response) 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 

 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 