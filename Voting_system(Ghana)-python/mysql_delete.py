import mysql.connector


def delete_column(db_config, table, column):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Prepare the SQL query to delete the column
        query = f"ALTER TABLE {table} DROP COLUMN {column}"
        cursor.execute(query)

        # Commit the changes
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        print(f"Column {column} deleted successfully from {table}.")
    except mysql.connector.Error as e:
        print(f"Error: {e}")


def delete_row(db_config, table, condition):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Prepare the SQL query to delete the row
        query = f"DELETE FROM {table} WHERE {condition}"
        cursor.execute(query)

        # Commit the changes
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        print(f"Row deleted successfully from {table}.")
    except mysql.connector.Error as e:
        print(f"Error: {e}")
