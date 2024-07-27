from application import app
import json
from flask import Flask,request,jsonify
from application.models.userModels import checkToken,updateUserBMI
from application.models.foodModels import getFoodCat,createUserFavFoodCat,getUserFavFoodCat,updateUserFavFoodCat

@app.route('/foodCat', methods = ['POST'])
def foodCat():
    token = request.form['token']
    data = checkToken(token)
    if data is not None:
        foodCat = getFoodCat()
        data = {
            "foodCat" : foodCat
        }
        return jsonify({"message": "Success","data":data,"rc":"00"}), 201
    else:
        return jsonify({"error": "Unauthorized Access","rc":"500"}), 400

@app.route('/userFavFoodCat', methods = ['POST'])
def userFavFoodCat():
    token = request.form['token']
    data = checkToken(token)
    if data is not None:
        userFoodFavCat = getUserFavFoodCat(data[0])
        if userFoodFavCat is not None :
            userFavFoodCat = json.loads(userFoodFavCat[2])  # Parse JSON string into a list
            userFoodFavCat = list(set(userFavFoodCat))
            
            userFavFoodCatData = {
                "userFoodFavCat" : userFoodFavCat
            }

            return jsonify({"message": "Success","data":userFavFoodCatData,"rc":"00"}), 201
        else :
            return jsonify({"error": "Data Not Found","rc":"404"}), 404
    else:
        return jsonify({"error": "Unauthorized Access","rc":"500"}), 400

@app.route('/updateBMI', methods = ['POST'])
def updateBMI():
    token = request.form['token']
    data = checkToken(token)
    if data is not None:
        bb = request.form['bb']
        tb = request.form['tb']
        tb = float(tb) / 100  # convert from cm to m
        BMI = float(bb) / (tb * tb)  # calculate BMI
        print(BMI)
        userId = data[0]
        if updateUserBMI(userId,BMI,bb,tb) :
            newData = checkToken(token)
            data = {
                "id": newData[0],
                "fullName": newData[1],
                "email": newData[2],
                "phoneNo" : newData[3],
                "token" : token,
                "BMI" : newData[8]
            }
            return jsonify({"message": "Data updated","data":data,"rc":"00"}), 200
        else :
            return jsonify({"error": "Something when wrong","rc":"500"}), 500
    else:
        return jsonify({"error": "Unauthorized Access","rc":"500"}), 400

@app.route('/setUserFavFoodCat', methods = ['POST'])
def setUserFavFoodCat():
    token = request.form['token']
    data = checkToken(token)
    if data is not None:
        foodCat = request.form['foodCat']
        dataFavFood = {
            "user_id": data[0],
            "food_cat" : foodCat,
        }
        userFoodFavCat = getUserFavFoodCat(data[0])
        if userFoodFavCat is not None :
            if updateUserFavFoodCat(dataFavFood):
                return jsonify({"message": "Set User Favorite Categories Success","rc":"00"}), 201
            else:
                return jsonify({"error": "Failed to set user Favorite Categories Food","rc":"500"}), 500
        else :
            if createUserFavFoodCat(dataFavFood):
                return jsonify({"message": "Set User Favorite Categories Success","rc":"00"}), 201
            else:
                return jsonify({"error": "Failed to set user Favorite Categories Food","rc":"500"}), 500
    else:
        return jsonify({"error": "Unauthorized Access","rc":"500"}), 400
