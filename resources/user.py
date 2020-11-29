from flask_restful import Resource, reqparse
from flask import jsonify
import pymysql


parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')

class Users(Resource):
    def db_init(self):
        db = pymysql.connect('192.168.56.101',
                        'Tzujung','admin123', 'flask_demo')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    def get(self):
        db = pymysql.connect('192.168.56.101',
                'Tzujung','admin123', 'flask_demo')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = """Select * From flask_demo.users where deleted = False"""
        cursor.execute(sql)
        users = cursor.fetchall()
        db.close()
        response = {
            'data' : users
        }
        return jsonify(response)

    def post(self):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        user = {
        'name' : arg['name'],
        'gender' : arg['gender'],
        'birth' : arg['birth'] or '1900-01-01',
        'note' : arg['note'],
        }
        sql = """
            Insert into flask_demo.users
            (name, gender, birth, note)
            values('{}','{}','{}','{}')
        """.format(user['name'],user['gender'],user['birth']
                ,user['note'])
        result = cursor.execute(sql)
        db.commit()
        db.close()
        response = {
            'result': True
        }
        return jsonify(response)
class User(Resource):
    def db_init(self):
        db = pymysql.connect('192.168.56.101',
                        'Tzujung','admin123', 'flask_demo')
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor
    def get(self, id): #取單筆資料
        db, cursor = self.db_init()
        sql = """Select * From flask_demo.users
            where id = '{}'
        """.format(id)
        cursor.execute(sql)
        user = cursor.fetchall()
        response = {
            'data':user
        }
        db.close()
        response = {
        'data': user
    }
        return jsonify(response)
    #更改資料
    def patch(self,id): 
        db, cursor = self.db_init()
        arg = parser.parse_args()
        user = {
        'name' : arg['name'],
        'gender' : arg['gender'],
        'birth' : arg['birth'] or '1900-01-01',
        'note' : arg['note'],
        }
        query = []
        for key, value in user.items():
            if value != None:
                query.append(key + ' =' + " '{}' ".format(value))
        query = ",".join(query)
        sql = """ Update flask_demo.users Set {} where id = "{}"
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
        sql = """Delete From flask_demo.users where id = '{}'
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
        sql = """Update flask_demo.users Set deleted = True where id = '{}'
        """.format(id)
        cursor.execute(sql)
        db.commit()
        db.close()
        response = {
            'result': True
        }
        return jsonify(response)