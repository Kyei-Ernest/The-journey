import random
import string
from datetime import datetime
import mysql.connector
from age_calc import age
import mysql_value_checker as vc
import mysql_delete as de
import bcrypt

# Database configurations
db_config_1 = {
    'user': 'root',
    'password': 'admin123',
    'host': 'localhost',
    'database': 'mydb'
}
db_config_2 = {
    'user': 'root',
    'password': 'admin123',
    'host': 'localhost',
    'database': 'gg'
}

conn = mysql.connector.connect(**db_config_1)
conn_1 = mysql.connector.connect(**db_config_2)

cur_1 = conn_1.cursor(buffered=True)
cur = conn.cursor(buffered=True)

# Global variables
legal_age = 0


# Voter registration class
class RegisterVoter:
    """
    Receives and validates the inputs of the voter.
    """

    def __init__(self, voter_id, name, contact, email, date_of_birth, personal_id, occupation, constituency, password,
                 conf_pass):
        """
                :param voter_id: unique identity characters assigned to each voter (this is randomly generated).
                :param name: the official name of the voter.
                :param contact: the phone number of the voter.
                :param email: the email address of the voter.
                :param date_of_birth: the official date of birth of the voter (e.g. 1/5/2005).
                :param personal_id: the nationality of the voter (must be Ghanaian).
                :param occupation: the current occupation of the voter.
                :param constituency: the constituency in relation to the current residence of the voter,
                                     from where he/she will cast his/her vote.
                """
        self.id = voter_id
        self.name = name
        self.date_of_birth = date_of_birth
        self.contact = contact
        self.email = email
        self.personal_id = personal_id
        self.occupation = occupation
        self.constituency = constituency
        self.password = password
        self.conf_pass = conf_pass

    def age_calculator(self):
        try:
            day, month, year = map(int, self.date_of_birth.split("/"))
            then = datetime(year=year, month=month, day=day)
            global legal_age
            legal_age = age(then)
        except ValueError as e:
            print(f"Error calculating age: {e}")
            return False

        return self.verification()

    def full_info(self):
        voter_info = {
            'ID': self.id,
            'Name': self.name,
            'Date of birth': self.date_of_birth,
            'Age': legal_age,
            'Contact': self.contact,
            'Email': self.email,
            'Personal ID': self.personal_id,
            'Occupation': self.occupation,
            'constituency': self.constituency,
        }
        try:
            hashed_password = RegisterVoter.create_hashed_password(self.password)
            python_date = datetime.strptime(self.date_of_birth, '%m/%d/%Y')
            mysql_date = python_date.strftime('%Y-%m-%d')

            sql = """INSERT INTO voterinfo(voter_id, name, contact, email, date_of_birth, personal_id, occupation,
                     constituency, voted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            val = (self.id, self.name, self.contact, self.email, mysql_date, self.personal_id,
                   self.occupation, self.constituency, 0,)
            cur.execute(sql, val)
            conn.commit()

            sql_1 = """INSERT INTO pass_table(voter_id, password) VALUES (%s, %s)"""
            val_1 = (self.id, hashed_password,)
            cur.execute(sql_1, val_1)
            conn.commit()

            # Display verified voter details
            for info in voter_info:
                print(f'{info}: {voter_info[info]}')

        except mysql.connector.Error as err:
            print(f"Error inserting into database: {err}")
            conn.rollback()
        except ValueError as e:
            print(f"Error parsing date: {e}")

    @staticmethod
    def create_hashed_password(password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def verification(self):
        try:
            # Checking if voter identification already exists
            id_exists = vc.check_value_exists(db_config_1, table='voterinfo', column='voter_id', user_input=self.id)
            # Checking if constituency exists
            const_exists = vc.check_value_exists(db_config_1, table='members_of_parliament', column='constituency',
                                                 user_input=self.constituency)
            # Check if personal_id exists
            exists = vc.check_value_exists(db_config_2, table='ecowas_identity', column='personal_id',
                                           user_input=self.personal_id)

            if id_exists:
                print("Sorry, this ID already exists for another voter")
                id_list = random.choices(string.ascii_uppercase + string.digits, k=8)
                self.id = "".join(id_list)
                return self.verification()
            elif legal_age < 18:
                print("You are not eligible for voting")
                return False
            elif not self.name or isinstance(self.name, int):
                print('Must enter a valid name')
                self.name = input("Name: ")
                return self.verification()
            elif not self.date_of_birth:
                print('Date of birth required')
                self.date_of_birth = input("Date of birth (e.g., 1/5/2005): ")
                return self.verification()
            elif not exists:
                print('Your ID does not exist in the database')
                return False
            elif not self.occupation:
                print('Occupation required')
                self.occupation = input("Occupation: ")
                return self.verification()
            elif not self.contact or len(self.contact) != 10:
                print("Contact must be exactly 10 digits")
                self.contact = input("Contact: ")
                return self.verification()
            elif not self.constituency or not const_exists:
                print('Constituency name entered does not exist')
                self.constituency = input("Constituency: ")
                return self.verification()
            elif self.password != self.conf_pass:
                print('The passwords you entered do not match')
                self.password = input('Password: ')
                self.conf_pass = input('Confirm Password: ')
                return self.verification()
            elif len(self.password) < 10 or len(self.conf_pass) < 10:
                print('Password must contain more than 10 characters.')
                self.password = input('Password: ')
                self.conf_pass = input('Confirm Password: ')
                return self.verification()
            else:
                self.full_info()
                return True

        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            return False
        except Exception as e:
            print(f"Error during verification: {e}")
            return False


# Class for registering presidential candidates
class RegisterPresident:
    """
    Receives and stores inputs about presidential candidates
    """

    def __init__(self, political_party, presidential_candidate_name):
        self.political_party = political_party
        self.presidential_candidate_name = presidential_candidate_name

    def store_pres_info(self):
        try:
            # Store presidential candidate info in database
            sql = "INSERT INTO presidents(political_party, presidential_candidate_name) VALUES (%s, %s)"
            val = (self.political_party, self.presidential_candidate_name)
            cur.execute(sql, val)

            # Create a new column with the political party name in 'members_of_parliament' table
            table = 'members_of_parliament'
            new_column = self.political_party
            query = f"ALTER TABLE {table} ADD COLUMN {new_column} VARCHAR(255)"
            cur.execute(query)
            conn.commit()

        except mysql.connector.Error as err:
            print(f"Error storing presidential candidate info: {err}")
            conn.rollback()
        except Exception as e:
            print(f"An error occurred: {e}")


# Class for registering parliamentary candidates
class RegisterMP(RegisterPresident):
    """
    Receives input and stores details about parliamentary candidates
    """

    def __init__(self, constituency, political_party="", presidential_candidate_name=""):
        super().__init__(political_party, presidential_candidate_name)
        self.constituency = constituency

    def store_mp_info(self):
        try:
            # Check if constituency exists in 'members_of_parliament'
            cur.execute("SELECT constituency FROM mydb.members_of_parliament WHERE constituency LIKE %s;",
                        (self.constituency,))
            results = cur.fetchone()

            if results is None:
                # Insert constituency if it doesn't exist
                sql = "INSERT INTO members_of_parliament(constituency) VALUES (%s)"
                val = (self.constituency,)
                cur.execute(sql, val)
                conn.commit()
                print("Constituency successfully added.")
            else:
                print("Constituency already exists in database.")

        except mysql.connector.Error as err:
            print(f"Error storing parliamentary candidate info: {err}")
            conn.rollback()
        except Exception as e:
            print(f"An error occurred: {e}")


# Function to start other registration processes
def start_other_registration():
    try:
        while True:
            choose = input("""
1. Add presidential candidate
2. Add constituency
3. Add parliamentary candidate
4. Exit
Enter your choice: """)

            if choose == '1':
                # Add presidential candidate
                while True:
                    political_party = input("Enter political party: ")
                    poli_party_exist = vc.check_value_exists(db_config_1, 'presidents',
                                                             'political_party', political_party)
                    if poli_party_exist:
                        print('This political party is already represented.')
                    else:
                        presidential_candidate_name = input("Enter presidential candidate name: ")
                        spr = RegisterPresident(political_party=political_party,
                                                presidential_candidate_name=presidential_candidate_name)
                        spr.store_pres_info()
                        break

            elif choose == '2':
                # Add constituency
                constituency = input("Enter constituency name: ")
                smpr = RegisterMP(constituency=constituency)
                smpr.store_mp_info()

            elif choose == '3':
                # Add parliamentary candidate
                pp_or_ind = input("""Candidate is
1. Affiliated with a political party
2. Independent
Enter your choice: """)
                if pp_or_ind == "1":
                    # Delete 'None' columns if any (this logic needs review)
                    de.delete_column(db_config_1, column='None', table='members_of_parliament')
                    const_name = input("Enter constituency name: ").casefold()
                    # Check if constituency exists in database
                    const_valid = vc.check_value_exists(db_config_1, table='members_of_parliament',
                                                        column='constituency', user_input=const_name)
                    if const_valid:
                        while True:
                            pp_name = input("Enter political party name: ").casefold()
                            pp_exist = vc.check_column_exists(db_config_1, 'members_of_parliament', pp_name)
                            if pp_exist:
                                mp_name = input("Enter candidate name: ")
                                sql = f'UPDATE members_of_parliament SET {pp_name} = %s WHERE constituency = %s'
                                var = (mp_name, const_name)
                                cur.execute(sql, var)
                                conn.commit()
                                break
                            else:
                                print("Political Party you entered does not exist in the database.")
                                break
                    else:
                        print("Constituency does not exist.")

                elif pp_or_ind == "2":
                    # Delete 'None' columns if any (this logic needs review)
                    de.delete_column(db_config_1, column='None', table='members_of_parliament')
                    constituency_name = input("Enter constituency name: ")
                    const_valid = vc.check_value_exists(db_config_1, table='members_of_parliament',
                                                        column='constituency', user_input=constituency_name)
                    if const_valid:
                        candidate_name = input("Enter candidate name: ")
                        for count in range(1, 10):
                            column_name = f"independent{count}"
                            col_exist = vc.check_column_exists(db_config_1, table_name='members_of_parliament',
                                                               column_name=column_name)
                            if col_exist is False:
                                cur.execute(f"ALTER TABLE members_of_parliament ADD COLUMN {column_name} VARCHAR(255)")
                                sql = (f"UPDATE members_of_parliament SET {column_name} = '{candidate_name}' "
                                       f"WHERE constituency = '{constituency_name}'")
                                cur.execute(sql)
                                conn.commit()
                                break
                            else:
                                sql = (f"SELECT * FROM members_of_parliament WHERE constituency = %s AND"
                                       f" {column_name} IS NULL")
                                cur.execute(sql, (constituency_name,))
                                result = cur.fetchone()
                                if result is not None:
                                    sql = (f"UPDATE members_of_parliament SET {column_name} = '{candidate_name}'"
                                           f" WHERE constituency = '{constituency_name}'")
                                    cur.execute(sql)
                                    conn.commit()
                                    break
                                else:
                                    pass
                    else:
                        print("Constituency does not exist.")

                else:
                    break
            elif choose == '4':
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please enter a number from 1 to 4.")

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Function to start the voter registration process
def start_voter_registration_process():
    try:
        while True:
            choice = input("""
1. Register
2. Exit
Enter your choice: """)

            if choice == "1":
                id_list = random.choices(string.ascii_uppercase + string.digits, k=8)
                ID = "".join(id_list)
                name = input('Full Name: ')
                dob = input('Date of birth (e.g., 1/5/2005): ')
                contact = input('Contact: ')
                email = input('Email: ')
                personal_id = input('Personal ID: ')
                occupation = input('Occupation: ')
                constituency = input('Constituency: ')
                password = input('Password: ')
                confirm = input('Confirm Password: ')

                svrp = RegisterVoter(
                    voter_id=ID,
                    name=name,
                    date_of_birth=dob,
                    contact=contact,
                    email=email,
                    personal_id=personal_id,
                    occupation=occupation,
                    constituency=constituency,
                    password=password,
                    conf_pass=confirm
                )
                svrp.age_calculator()
                break

            elif choice == "2":
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please enter 1 or 2.")

    except Exception as e:
        print(f"An error occurred: {e}")
