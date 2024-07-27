from application.config.database import get_connection, get_cursor
from datetime import datetime

def createUsers(data):
    connection = get_connection()
    if connection is not None:
        cursor = get_cursor(connection)
        if cursor is not None:
            try:
                # Define the SQL query to insert a new user
                sql = """
                INSERT INTO h_users (fullName, email, phoneNo, password, createdTime)
                VALUES (%s, %s, %s, %s, %s)
                """
                # Format the datetime object to a string
                created_time_str = data['createdTime'].strftime('%Y-%m-%d %H:%M:%S')

                # Execute the query with user data
                cursor.execute(sql, (data['fullName'], data['email'], data['phoneNo'], data['password'], created_time_str))

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

def checkUsers(email, phoneNo):
    connection = get_connection()
    if connection is not None:
        cursor = get_cursor(connection)
        if cursor is not None:
            try:
                # Query to check if the email or phone number exists
                sql = """
                SELECT COUNT(*) FROM h_users WHERE email = %s OR phoneNo = %s
                """
                cursor.execute(sql, (email, phoneNo))
                result = cursor.fetchone()
                return result[0] > 0
            except Exception as e:
                print(f"An error occurred: {e}")
                return True  # Return True to indicate an error occurred
            finally:
                cursor.close()
                connection.close()
    return False

def checkToken(token):
    connection = get_connection()
    if connection is not None:
        cursor = get_cursor(connection)
        if cursor is not None:
            try:
                # Query to check if the token exists
                sql = """
                SELECT * FROM h_users WHERE token = %s
                """
                cursor.execute(sql, (token,))  # Wrap token in a tuple
                result = cursor.fetchone()
                return result  # Return True if token exists, otherwise False
            except Exception as e:
                print(f"An error occurred: {e}")
                return False  # Return False to indicate an error occurred
            finally:
                cursor.close()
                connection.close()
    return False  # Return False if the connection or cursor is None

def getUsers(email, password):
    connection = get_connection()
    if connection is not None:
        cursor = get_cursor(connection)
        if cursor is not None:
            try:
                # Query to check if the email and hashed password exists
                sql = """
                SELECT * FROM h_users WHERE email = %s and password = %s
                """
                cursor.execute(sql, (email, password))
                result = cursor.fetchone()
                return result  # Return the result (None if no user found)
            except Exception as e:
                print(f"An error occurred: {e}")
                return None  # Return None to indicate an error occurred
            finally:
                cursor.close()
                connection.close()
    return None

def updateToken(id, token):
    connection = get_connection()
    if connection is not None:
        cursor = get_cursor(connection)
        if cursor is not None:
            try:
                # Query to update the token for the specified user ID
                sql = """
                UPDATE h_users SET token = %s WHERE id = %s
                """
                cursor.execute(sql, (token, id))
                connection.commit()  # Commit the transaction
                return True  # Return True if a row was updated
            except Exception as e:
                print(f"An error occurred: {e}")
                return False  # Return False to indicate an error occurred
            finally:
                cursor.close()
                connection.close()
    return False  # Return False if the connection or cursor is None

def updateUserBMI(id, BMI, bb, tb):
    connection = get_connection()
    if connection is not None:
        cursor = get_cursor(connection)
        if cursor is not None:
            try:
                # Query to update the token for the specified user ID
                sql = """
                UPDATE h_users SET BMI=%s, bb=%s, tb=%s  WHERE id = %s
                """
                cursor.execute(sql, (BMI, bb, tb, id))
                connection.commit()  # Commit the transaction
                return True  # Return True if a row was updated
            except Exception as e:
                print(f"An error occurred: {e}")
                return False  # Return False to indicate an error occurred
            finally:
                cursor.close()
                connection.close()
    return False  # Return False if the connection or cursor is None
