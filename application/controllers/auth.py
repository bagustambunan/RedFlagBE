from application import app
from flask import Flask,request
from flask_hashing import Hashing

@app.route('/register', methods = ['POST'])

def index():
    fullName = request.form['fullName']
    email = request.form['email']
    phoneNumber = request.form['phoneNumber']
    password = request.form['password']
    hashPass = Hashing(password,salt="angelhack")

    return "ok"