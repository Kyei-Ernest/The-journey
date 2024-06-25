import mysql.connector
from mysql.connector import Error


# this functions checks whether a value exists in a particular column in a database table.
def check_value_exists(db_config, table, column, user_input):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(buffered=True)

        # Create a cursor object to execute SQL queries

        # Prepare the SQL query to check if the input value exists in the specified column
        query = f"SELECT COUNT(*) FROM {table} WHERE {column} = %s"
        cursor.execute(query, (user_input,))

        # Fetch the result
        result = cursor.fetchone()[0]

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Return True if the value exists, otherwise return False
        return result > 0

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return False


def check_column_exists(db_config, table_name, column_name):
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor = conn.cursor()

            # Query to get columns of the specified table
            cursor.execute(f"SHOW COLUMNS FROM {table_name};")
            columns = cursor.fetchall()

            # Check if column_name is in the list of columns
            column_exists = any(column[0] == column_name for column in columns)

            # Close the cursor and connection
            cursor.close()
            conn.close()

            return column_exists

    except Error as e:
        print(f"Error: {e}")
        return False
