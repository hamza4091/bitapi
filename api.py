import pymysql
from app import app
from config import mysql
from flask import jsonify, request
from flask import flash, request
import json
import base64
import os
import cv2


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
        response = jsonify(message=rows, id=cursor.lastrowid)
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
        conn = mysql.connect()
        cursor = conn.cursor()
        insert_user_cmd = """INSERT INTO signup_data (name, password, designation)
                                           VALUES(%s, %s, %s)"""
        cursor.execute(insert_user_cmd, (name, password, designation))
        conn.commit()
        response = jsonify(message='User added successfully.', id=cursor.lastrowid)
        # response.data = cursor.lastrowid
        response.status_code = 200
        return response
    else:
        return 'Content-Type not supported!'


if __name__ == "__main__":
    app.run(port=1234, debug=True)
