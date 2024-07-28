from application import app
import json
from flask import Flask,request,jsonify
from application.models.userModels import checkToken,updateUserBMI
from application.models.foodModels import getFoodCat,createUserFavFoodCat,getUserFavFoodCat,updateUserFavFoodCat,getFood,getFilterFood,getFoodById
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
import joblib

@app.route('/foodCat', methods = ['POST'])
def foodCat():
    token = request.form['token']
    data = checkToken(token)
    if data is not None:
        foodCat = getFoodCat()
        data = {
            "foodCat" : foodCat
        }
        return jsonify({"message": "Success","data":data,"rc":"00"}), 200
    else:
        return jsonify({"error": "Unauthorized Access","rc":"500"}), 400

@app.route('/food', methods = ['POST'])
def food():
    token = request.form['token']
    data = checkToken(token)
    if data is not None:
        food = getFood()
        # Process food categories
        cleaned_food_data = []
        for item in food:
            item_list = list(item)  # Convert tuple to list
            item_list[2] = json.loads(item_list[2])  # Decode the JSON string
            # Create cleaned data object
            cleaned_data = {
                "foodId": item_list[0],
                "foodName": item_list[1],
                "foodCat": item_list[2],
                "foodCal": item_list[3],
            }
            cleaned_food_data.append(cleaned_data)
        
        data = {
            "food": cleaned_food_data
        }
        return jsonify({"message": "Success","data":data,"rc":"00"}), 200
    else:
        return jsonify({"error": "Unauthorized Access","rc":"500"}), 400

@app.route('/getFoodById', methods = ['POST'])
def getFoodId():
    token = request.form['token']
    data = checkToken(token)
    if data is not None:
        foodId = request.form['foodId']
        print(foodId)
        food = getFoodById(foodId)
        if food is not None :
            foodCat = json.loads(food[2])  # Parse JSON string into a list
            foodCat = list(set(foodCat))

            cleaned_data = {
                "foodId": food[0],
                "foodName": food[1],
                "foodCat": foodCat,
                "foodCal": food[3],
            }
            data = {
                "food": cleaned_data
            }
            return jsonify({"message": "Success","data":data,"rc":"00"}), 200
        else:
            return jsonify({"error": "Data not found","rc":"404"}), 404
    else:
        return jsonify({"error": "Unauthorized Access","rc":"500"}), 400

@app.route('/filterFood', methods = ['POST'])
def filterFood():
    token = request.form['token']
    data = checkToken(token)
    if data is not None:
        userFoodFavCat = getUserFavFoodCat(data[0])
        if userFoodFavCat is not None :
            userFavFoodCat = json.loads(userFoodFavCat[2])  # Parse JSON string into a list
            userFoodFavCat = list(set(userFavFoodCat))

            food = getFilterFood(userFoodFavCat)
            # Process food categories
            cleaned_food_data = []
            for item in food:
                item_list = list(item)  # Convert tuple to list
                item_list[2] = json.loads(item_list[2])  # Decode the JSON string
                
                # Create cleaned data object
                cleaned_data = {
                    "foodId": item_list[0],
                    "foodName": item_list[1],
                    "foodCat": item_list[2],
                    "foodCal": item_list[3],
                }
                cleaned_food_data.append(cleaned_data)
            
            data = {
                "food": cleaned_food_data
            }
            return jsonify({"message": "Success","data":data,"rc":"00"}), 200
        else:
            return jsonify({"error": "You must fill the favorite food categories","rc":"404"}), 404
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

            return jsonify({"message": "Success","data":userFavFoodCatData,"rc":"00"}), 200
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
        userId = data[0]
        if updateUserBMI(userId,BMI,bb,tb) :
            newData = checkToken(token)
            data = {
                "id": newData[0],
                "fullName": newData[1],
                "email": newData[2],
                "phoneNo" : newData[3],
                "token" : token,
                "BMI" : newData[8],
                "bb" : newData[9],
                "tb" : newData[10]
            }
            return jsonify({"message": "Data updated","data":data,"rc":"00"}), 201
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


@app.route('/getFoodMenu', methods=['POST'])
def getRecomendedFoodMenu():
    token = request.form['token']
    data = checkToken(token)
    if data is not None:
        BMI = data[8]
        userFoodFavCat = getUserFavFoodCat(data[0])
        userFavFoodCat = json.loads(userFoodFavCat[2])  # Parse JSON string into a list
        userFoodFavCat = list(set(userFavFoodCat))

        food = getFilterFood(userFoodFavCat)
        # Process food categories
        cleaned_food_data = []
        for item in food:
            item_list = list(item)  # Convert tuple to list
            item_list[2] = json.loads(item_list[2])  # Decode the JSON string
            
            # Create cleaned data object
            cleaned_data = {
                "foodId": item_list[0],
                "foodName": item_list[1],
                "foodCat": item_list[2],
                "foodCal": item_list[3],
            }
            cleaned_food_data.append(cleaned_data)
        
        recomend = recommend_food(BMI, userFoodFavCat, cleaned_food_data)
        
        # No need to call to_dict, just return the list
        return jsonify({"message": "Success", "data": recomend, "rc": "00"}), 200
    else:
        return jsonify({"error": "Unauthorized Access", "rc": "500"}), 400

def recommend_food(bmi, preferred_categories, foodData):
    df = pd.DataFrame(foodData)

    if bmi < 18.5:
        calorie_needs = 2000
    elif 18.5 <= bmi < 24.9:
        calorie_needs = 2500
    else:
        calorie_needs = 3000
    
    # Filter foods based on preferred categories
    filtered_foods = df[df['foodCat'].apply(lambda x: any(cat in x for cat in preferred_categories))]
    
    # Shuffle the results to provide variety
    filtered_foods = filtered_foods.sample(frac=1).reset_index(drop=True)
    
    # Select foods that meet calorie needs
    recommended_foods = []
    total_calories = 0
    for _, food in filtered_foods.iterrows():
        if total_calories + food['foodCal'] <= calorie_needs:
            recommended_foods.append(food.to_dict())
            total_calories += food['foodCal']
        if len(recommended_foods) == 3:
            break
    
    return recommended_foods