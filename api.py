import pymysql
from app import app
from config import mysql
from flask import jsonify, request
from flask import flash, request
import json
import base64
import os
import cv2
import base64




@app.route('/get', methods=['GET'])
def get():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("select * from visitor_data")
    rows = cur.fetchall()
    resp = json.dumps(rows, indent=4, sort_keys=True, default=str)
    return resp

@app.route('/insert', methods=['POST'])
def insert():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        name = request.json['name']
        cnic = request.json['cnic']
        phone = request.json['phone']
        destination = request.json['destination']
        date = request.json['date']
        time = request.json['time']
        image = request.json['image']
        x = image.split(",")[1]
        base64_image = str.encode(x)
        with open(os.path.join("./images", name + ".png"), "wb") as fh:
            fh.write(base64.decodebytes(base64_image))
        conn = mysql.connect()
        cursor = conn.cursor()
        insert_user_cmd = """INSERT INTO visitor_data (name, cnic, phone,destination,date,time,image)
                                           VALUES(%s, %s, %s,%s,%s,%s,%s)"""
        cursor.execute(insert_user_cmd, (name, cnic, phone, destination, date, time, image))
        conn.commit()
        response = jsonify(message='User added successfully.', id=cursor.lastrowid)
        # response.data = cursor.lastrowid
        response.status_code = 200
        return response
    else:
        return 'Content-Type not supported!'


@app.route('/login', methods=['POST'])
def login():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        name = request.json['name']
        password = request.json['password']
        conn = mysql.connect()
        cursor = conn.cursor()
        query = ' select designation as designation  from signup_data where name = %s and password = %s'
        tuple = (name, password)
        cursor.execute(query, tuple)
        rows = cursor.fetchall()
        conn.commit()
        resp = json.dumps(rows, indent=4, sort_keys=True, default=str)
        response = jsonify(rows[0][0])
        # response.data = cursor.lastrowid
        response.status_code = 200
        return response
    else:
        return 'Content-Type not supported!'


@app.route('/signup', methods=['POST'])
def signup():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        name = request.json['name']
        password = request.json['password']
        designation = request.json['designation']
        try:
            email = request.json['email']
            image = request.json['image']
        except:
            print("An exception occurred")
            email = "Null"
            image = "Null"

        conn = mysql.connect()
        cursor = conn.cursor()
        if email =="Null":
            insert_user_cmd = """INSERT INTO signup_data (name, password, designation)
                                                      VALUES(%s, %s, %s)"""
            cursor.execute(insert_user_cmd, (name, password, designation))
        else:
            insert_user_cmd = """INSERT INTO signup_data (name, password, designation,email,image)
                                                      VALUES(%s, %s, %s,%s,%s)"""
            cursor.execute(insert_user_cmd, (name, password, designation, email,image))

        conn.commit()
        response = jsonify(message='User added successfully.', id=cursor.lastrowid)
        # response.data = cursor.lastrowid
        response.status_code = 200
        return response
    else:
        return 'Content-Type not supported!'


@app.route('/saveAlerts/<string:name>/<int:status>', methods=['POST'])
def Alertdata(name, status):
    conn = mysql.connect()
    cursor = conn.cursor()
    # insert_user_cmd = """insert into Alerts values(%s,%s)"""
    cursor.execute("insert into alerts (name,status) values ('" + (name) + "' ,'" + str(status) + "')")
    cursor.commit()
    response = ('data added successfully.')
    # response.data = cursor.lastrowid
    return response


@app.route('/getNames', methods=['GET'])
def getAlertData():
    conn = mysql.connect()
    d = []
    cur = conn.cursor()
    cur.execute("select * from alerts")
    rows = cur.fetchall()
    i = 1
    for row in rows:
        l = {'name': row[0], 'status': row[1].strip()}
        d.append(l)
        i += 1
    # resp = json.dumps(d,default=str)
    # resp=json.loads(resp)
    return jsonify(d)


@app.route('/getAlertVisitor/<string:name>', methods=['GET'])
def getAlertVisitor(name):
    conn = mysql.connect()
    d = []
    cur = conn.cursor()
    cur.execute("select * from visitor_data where name='" + (name) + "'")
    rows = cur.fetchall()
    for row in rows:
        l = {'name': row[0], 'cnic': row[1], 'phone': row[2], 'destination': row[3],"date":row[4],"image": base64.b64encode(row[6]).decode()}
        d.append(l)
    return jsonify(d)


if __name__ == "__main__":
    app.run(port=1234, debug=True)
