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
