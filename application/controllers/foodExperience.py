from application import app
from flask import Flask,request,jsonify
from application.models.userModels import checkToken
from application.models.foodModels import getFoodCat

@app.route('/foodCat', methods = ['POST'])
def foodCat():
    token = request.form['token']
    data = checkToken(token)
    if checkToken(token) is not None:
        foodCat = getFoodCat()
        data = {
            "foodCat" : foodCat
        }
        return jsonify({"message": "success","data":data,"rc":"00"}), 201
    else:
        return jsonify({"error": "Unauthorized Access","rc":"500"}), 400

@app.route('/addFoodCat', methods = ['POST'])
def addFoodCat():
    token = request.form['token']
    if checkToken(token):
        foodCat = getFoodCat()
        data = {
            "foodCat" : foodCat
        }
        return jsonify({"message": "success","data":data,"rc":"00"}), 201
    else:
        return jsonify({"error": "Unauthorized Access","rc":"500"}), 400
