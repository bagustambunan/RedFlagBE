from application import app
from flask import Flask,request,jsonify
from application.models.userModels import createUsers,checkUsers,getUsers,updateToken
import hashlib
import re
from datetime import datetime
import random

@app.route('/', methods = ['GET'])
def index():
    return "success"

@app.route('/register', methods = ['POST'])
def register():
    fullName = request.form['fullName']
    email = request.form['email']
    phoneNo = request.form['phoneNo']
    password = request.form['password']

    # Email validation
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        return jsonify({"error": "Invalid email format","rc":"500"}), 400

    # Phone number validation (assuming it should be 10 digits)
    phone_regex = r'^\d{10,15}$'
    if not re.match(phone_regex, phoneNo):
        return jsonify({"error": "Invalid phone number format","rc":"500"}), 400

    # Check if email or phone number already exists
    if checkUsers(email, phoneNo):
        return jsonify({"error": "Email or phone number already exists","rc":"500"}), 400

    hash_object = hashlib.sha1(password.encode())
    hashPass = hash_object.hexdigest()

    data = {
        "fullName": fullName,
        "email": email,
        "password": hashPass,
        "phoneNo" : phoneNo,
        "createdTime": datetime.now()
    }

    if createUsers(data):
        return jsonify({"message": "User registered successfully","rc":"00"}), 201
    else:
        return jsonify({"error": "Failed to register user","rc":"500"}), 500

@app.route('/login', methods = ['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    hash_object = hashlib.sha1(password.encode())
    hashPass = hash_object.hexdigest()

    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        return jsonify({"error": "Invalid email format","rc":"500"}), 400

    # Check if email or phone number already exists
    result = getUsers(email, hashPass)
    if result:   
        id = result[0]
        rand = random.randint(1,99999)
        combine = f"{id}{rand}"
        hash_object = hashlib.sha1(combine.encode())
        token = hash_object.hexdigest()
        
        if updateToken(id,token) is True:
            data = {
                "id": result[0],
                "fullName": result[1],
                "email": result[2],
                "phoneNo" : result[3],
                "token" : token
            }
            return jsonify({"message": "Login Success","data":data,"rc":"00"}), 200
        else :
            return jsonify({"error": "Something when wrong","rc":"500"}), 500
    else:
        return jsonify({"error": "Failed to login","rc":"500"}), 500