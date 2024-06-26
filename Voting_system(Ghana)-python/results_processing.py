# results verification
import mysql.connector

conn = mysql.connector.connect(host="127.0.0.1", user="root", password="admin123", database="mydb")
cur = conn.cursor()

table = ''
# count votes for each presidential candidate
def president_vote_count():
    try:
        # Query to select all president IDs from the presidents table
        select_presidents_sql = "SELECT ID FROM presidents"
        cur.execute(select_presidents_sql)
        presidents = cur.fetchall()
        # Loop through each president
        for president in presidents:
            president_id = president[0]

            # Query to count votes for the current president
            count_votes_sql = "SELECT COUNT(*) FROM voterinfo WHERE president_vote = %s"
            cur.execute(count_votes_sql, (president_id,))
            votes_count = cur.fetchone()[0]

            # Update the number of votes for the current president
            update_votes_sql = "UPDATE presidents SET number_of_votes = %s WHERE ID = %s"
            cur.execute(update_votes_sql, (votes_count, president_id))
            conn.commit()

            # Query to count the total number of votes cast
            count_total_votes_sql = "SELECT COUNT(*) FROM voterinfo WHERE voted = '1'"
            cur.execute(count_total_votes_sql)
            total_votes_count = cur.fetchone()[0]

            # Calculate the vote percentage for the current president
            vote_percentage = round((votes_count / total_votes_count) * 100, 1) if total_votes_count > 0 else 0

            # Update the vote percentage for the current president
            update_percentage_sql = "UPDATE presidents SET vote_percentage = %s WHERE ID = %s"
            cur.execute(update_percentage_sql, (f"{vote_percentage}%", president_id))
            conn.commit()
    except Exception as e:
        # Rollback in case of any error
        conn.rollback()
        # Log the error (print statement used here, but consider using logging framework)
        print(f"An error occurred: {e}")


def create_table_if_not_exists(table_name):
    try:
        # Fetching the names of MP candidates from 'members_of_parliament' table
        fetch_table = 'members_of_parliament'
        query = f"SELECT * FROM {fetch_table} WHERE constituency = %s"
        cur.execute(query, (table_name,))
        result = cur.fetchone()

        if result is None:
            print(f"No data found for constituency '{table_name}'.")
            return

        container = []
        result_length = len(result)

        # Collect the result into a container
        for row in result:
            container.append(row)

        # Check if the table already exists
        cur.execute(f"SHOW TABLES LIKE '{table_name}'")
        result = cur.fetchone()

        if not result:  # if table does not exist
            table_schema = "id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), number_of_votes INT"
            cur.execute(f"CREATE TABLE {table_name} ({table_schema})")

            # Insert data into the new table, assuming relevant data starts from the 3rd column
            for index in range(2, result_length):
                data_to_insert = container[index]
                insert_name_into_new_table(table_name, data_to_insert)
        else:
            # Insert data into the existing table, assuming relevant data starts from the 3rd column
            for index in range(2, result_length):
                data_to_insert = container[index]
                insert_name_into_existing_table(table_name, data_to_insert)

    except Exception as e:
        # Rollback in case of any error
        conn.rollback()
        # Log the error (print statement used here, but consider using logging framework)
        print(f"An error occurred: {e}")


def insert_name_into_existing_table(table_name, data_to_check):
    if data_to_check is not None:
        column_name = 'name'
        # SQL query to check if data exists in the column
        check_query = f"SELECT EXISTS(SELECT 1 FROM {table_name} WHERE {column_name} = %s)"
        cur.execute(check_query, (data_to_check,))
        exists = cur.fetchone()[0]

        if not exists:
            # SQL query to insert data if it does not exist
            insert_query = f"INSERT INTO {table_name} ({column_name}) VALUES (%s)"
            cur.execute(insert_query, (data_to_check,))
            conn.commit()
            print("Data inserted successfully.")
        else:
            pass


def insert_name_into_new_table(table_name, data):
    column_name = 'name'
    if data is not None:
        query = f"INSERT INTO {table_name} ({column_name}) VALUES (%s)"
        try:
            cur.execute(query, (data,))
            conn.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            conn.rollback()  # Rollback the transaction in case of an error


def insert_vcounts_into_table(constituency, mp_id):
    fetch_table = 'voterinfo'
    try:
        # Prepare the SQL query to select all records from the specified row
        query = f"SELECT count(*) FROM {fetch_table} WHERE constituency = %s and mp_vote = %s"
        cur.execute(query, (constituency, mp_id,))
        result = cur.fetchone()

        if result:
            query = f"UPDATE {constituency} SET number_of_votes = %s WHERE id = %s"
            cur.execute(query, (result[0], mp_id))
            conn.commit()
        else:
            print(f"No results found for constituency '{constituency}' and mp_id '{mp_id}'.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()  # Rollback the transaction in case of an error


def mp_vote_count():
    try:
        query = "SELECT constituency FROM members_of_parliament"
        cur.execute(query)
        results = cur.fetchall()

        for row in results:
            global table
            table = row[0]
            create_table_if_not_exists(table)

            query_1 = f"SELECT id FROM {table}"
            cur.execute(query_1)
            result_1 = cur.fetchall()

            for row_3 in result_1:
                insert_vcounts_into_table(table, row_3[0])


    except mysql.connector.Error as err:
        print(f"Error: {err}")




def display_results():
    try:
        print(f'\n-Presidential vote results ')
        # fetch presidential results from database
        pres_query = "SELECT * FROM presidents"
        cur.execute(pres_query)
        pres_results = cur.fetchall()
        for LIST in pres_results:
            print(f'{LIST[0]}   |{LIST[1]}  - {LIST[2]}   |{LIST[3]}| - {LIST[4]}')

        mp_vote_count()
        print(f'\n-MP vote results for {table} constituency')
        # fetch mp results from database
        mp_query = f"SELECT * FROM {table}"
        cur.execute(mp_query)
        mp_results = cur.fetchall()
        for LIST in mp_results:
            print(f'{LIST[0]}   |{LIST[1]}  - |{LIST[2]}|')

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Ensure that the cursor and connection are closed properly
        cur.close()
        conn.close()



