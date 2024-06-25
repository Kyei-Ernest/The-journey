import ballot_creation as bc
import mysql.connector
import psycopg2
import bcrypt

pc = bc

conn = mysql.connector.connect(host="127.0.0.1", user="root", password="admin123", database="mydb")
cur = conn.cursor()
voters_id = ""


def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode(), stored_password)


def vote_mp():
    """Display the Member of Parliament candidates list and cast vote"""
    global voters_id
    voters_id = input("Enter voter ID ")
    votesql = f""" select voted from voterinfo where voter_id = (%s)"""
    votevar = (voters_id,)
    cur.execute(votesql, votevar)
    voted = cur.fetchall()
    voted_already = True
    for item in voted:
        voted_already = item[0]

    if not voted_already:
        password = input('Enter password: ')
        pass_query = f""" select password from pass_table where voter_id = (%s)"""
        pass_var = (voters_id,)
        cur.execute(pass_query, pass_var)
        pw = cur.fetchone()
        for pwd in pw:
            pwd_bytes = pwd.encode('utf-8')
            is_valid = verify_password(pwd_bytes, password)
            if is_valid:
                bc.file_existence_and_mpdisplay(voters_id)
                voter_choice_mp = input("Cast vote ->> ")
                sql = f"update voterinfo set mp_vote = (%s) where voter_id = (%s)"
                var = (voter_choice_mp, voters_id)
                cur.execute(sql, var)
                conn.commit()
                return vote_president()
            else:
                print('Incorrect password or ID')

    else:
        print("Sorry, but it seems you have casted your vote already")


def vote_president():
    """Display the presidential candidates list and cast vote"""
    try:
        # Display the list of presidential candidates
        pc.display_presidents()

        # Prompt the voter to cast their vote
        voter_choice_president = input("Cast vote ->> ")

        # Ensure the input is valid (you might want to add more validation here)
        if not voter_choice_president:
            raise ValueError("Invalid vote. Please enter a valid candidate.")

        # Update the vote in the database
        sql = "UPDATE voterinfo SET president_vote = (%s) WHERE voter_id = (%s)"
        var = (voter_choice_president, voters_id)
        cur.execute(sql, var)

        # Mark the voter as having voted
        sql = "UPDATE voterinfo SET voted = 1 WHERE voter_id = (%s)"
        var = (voters_id,)
        cur.execute(sql, var)

        # Commit the transaction
        conn.commit()
        print("Vote successfully cast!")

    except ValueError as ve:
        print(f"Value Error: {ve}")

    except (psycopg2.DatabaseError, psycopg2.OperationalError) as db_err:
        print(f"Database Error: {db_err}")
        # Rollback in case of database error
        conn.rollback()

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # Rollback in case of any other error
        conn.rollback()


def display_poll():
    """Voter's confirmation to take part in the election"""
    while True:
        try:
            voter_entry = input("""Are you sure you want to vote now
    1. Yes
    2. No\n""")

            if voter_entry == "1":
                vote_mp()
                break
            elif voter_entry == "2":
                print("You have chosen not to vote at this time.")
                break
            else:
                raise ValueError("Invalid entry. Please enter 1 or 2.")

        except ValueError as ve:
            print(f"Error: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

