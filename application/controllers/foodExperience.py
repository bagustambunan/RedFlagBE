from application import app
from flask import Flask,request,jsonify
from application.models.userModels import checkToken,updateUserBMI
from application.models.foodModels import getFoodCat

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

@app.route('/addUserFoodCat', methods = ['POST'])
def addFoodCat():
    token = request.form['token']
    data = checkToken(token)
    if data is not None:
        foodCat = request.form['foodCat']
    else:
        return jsonify({"error": "Unauthorized Access","rc":"500"}), 400
