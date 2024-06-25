import mysql.connector

# SQL statements for creating tables
create_voterinfo_table = """
CREATE TABLE IF NOT EXISTS voterinfo (
  Voter_id VARCHAR(255) PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  date_of_birth DATE,
  contact VARCHAR(255),
  email VARCHAR(255),
  personal_id VARCHAR(50),
  occupation VARCHAR(100),
  constituency VARCHAR(100),
  voted BOOLEAN DEFAULT FALSE,
  president_vote VARCHAR(255),
  mp_vote VARCHAR(255),
  password 
);
"""

create_president_table = """
CREATE TABLE IF NOT EXISTS presidents(
  id INT AUTO_INCREMENT PRIMARY KEY,
  political_party VARCHAR(100),
  presidential_candidate_name VARCHAR(255) NOT NULL,
  number_of_votes INT DEFAULT 0,
  vote_percentage VARCHAR(255)
);
"""

create_mpvotesinfo_table = """
CREATE TABLE IF NOT EXISTS members_of_parliament (
  id INT AUTO_INCREMENT PRIMARY KEY,
  constituency VARCHAR(100)
);
"""
create_pass_table = '''
CREATE TABLE IF NOT EXISTS pass_table (
    Voter_id VARCHAR(255),
    password VARCHAR(255),
    PRIMARY KEY (Voter_id),
    FOREIGN KEY (Voter_id) REFERENCES voterinfo(Voter_id)
);
'''

dbname = input("Enter database name")

mydb_connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="admin123",
)
cursor = mydb_connection.cursor()

cursor.execute("show databases")

database_list = cursor.fetchall()
for db in database_list:
    if dbname in db:
        print("The database name already exist. Use another unique name instead")
        break
    elif dbname == "":
        print("Your database schema must have a name")
        break
    else:
        try:

            # Connect to the database
            mydb = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="admin123",
                database=None
            )

            cursor = mydb.cursor()

            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE  {dbname} CHARACTER SET utf8 COLLATE utf8_general_ci;")

            mydb = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="admin123",
                database=dbname
            )
            cursor = mydb.cursor()

            # Execute table creation statements
            cursor.execute(create_voterinfo_table)
            cursor.execute(create_president_table)
            cursor.execute(create_mpvotesinfo_table)
            cursor.execute(create_pass_table)

            # Commit changes
            mydb.commit()

            print("Tables created successfully!")
            break

        except (mysql.connector.Error, mysql.connector.ProgrammingError) as err:
            print("Error creating tables:", err)
            break
