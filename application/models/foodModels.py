from application.config.database import get_connection, get_cursor

def getFoodCat():
    connection = get_connection()
    if connection is not None:
        cursor = get_cursor(connection)
        if cursor is not None:
            try:
                # Query to select all from h_food_cat
                sql = """
                SELECT * FROM h_food_cat
                """
                cursor.execute(sql)
                result = cursor.fetchall()  # Fetch all results
                return result  # Return the results (None if no rows found)
            except Exception as e:
                print(f"An error occurred: {e}")
                return None  # Return None to indicate an error occurred
            finally:
                cursor.close()
                connection.close()
    return None

def createUserFavFoodCat(data):
    connection = get_connection()
    if connection is not None:
        cursor = get_cursor(connection)
        if cursor is not None:
            try:
                # Define the SQL query to insert a new user
                sql = """
                INSERT INTO h_user_fav (user_id, food_cat)
                VALUES (%s, %s)
                """
                # Execute the query with user data
                cursor.execute(sql, (data['user_id'], data['food_cat']))
                # Commit the transaction
                connection.commit()
                return True
            except Exception as e:
                print(f"An error occurred: {e}")
                connection.rollback()  # Rollback the transaction in case of an error
                return False
            finally:
                # Close the cursor and connection
                cursor.close()
                connection.close()
    return False

def updateUserFavFoodCat(data):
    connection = get_connection()
    if connection is not None:
        cursor = get_cursor(connection)
        if cursor is not None:
            try:
                # Query to update the token for the specified user ID
                sql = """
                UPDATE h_user_fav SET food_cat=%s WHERE user_id=%s
                """
                # Execute the query with user data
                cursor.execute(sql, (data['food_cat'], data['user_id']))
                connection.commit()  # Commit the transaction
                return True  # Return True if a row was updated
            except Exception as e:
                print(f"An error occurred: {e}")
                return False  # Return False to indicate an error occurred
            finally:
                cursor.close()
                connection.close()
    return False  # Return False if the connection or cursor is None

def getUserFavFoodCat(user_id):
    connection = get_connection()
    if connection is not None:
        cursor = get_cursor(connection)
        if cursor is not None:
            try:
                # Query to check if the token exists
                sql = """
                SELECT * FROM h_user_fav WHERE user_id = %s
                """
                cursor.execute(sql, (user_id,))  # Wrap token in a tuple
                result = cursor.fetchone()
                return result  # Return True if token exists, otherwise False
            except Exception as e:
                print(f"An error occurred: {e}")
                return False  # Return False to indicate an error occurred
            finally:
                cursor.close()
                connection.close()
    return False  # Return False if the connection or cursor is None
