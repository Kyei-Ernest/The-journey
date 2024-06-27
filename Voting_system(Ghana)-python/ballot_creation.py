import mysql.connector
import mysql_value_checker as vc
from mysql.connector import Error

# Database configurations
db_config_1 = {
    'user': 'root',
    'password': 'admin123',
    'host': 'localhost',
    'database': 'mydb'
}
conn = mysql.connector.connect(**db_config_1)
cur = conn.cursor()


def display_presidents():
    """Display presidential candidates to voter"""
    try:
        print("** Vote for your preferred presidential candidate **")
        sql1 = "SELECT ID, political_party, presidential_candidate_name FROM presidents"
        cur.execute(sql1)
        myr1 = cur.fetchall()
        for x, y, z in myr1:
            print(f"{x} {y} - {z}")
    except Error as e:
        print(f"Error while retrieving presidential candidates: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def display_mp(voter_id):
    """Check the existence of the voter file and display MPs for the voter's constituency."""
    try:
        # Define the database table and column to check for voter ID
        table = 'voterinfo'
        column = 'voter_id'

        # Check if the voter ID exists in the database using a helper function
        voterid_exists = vc.check_value_exists(db_config_1, table, column, voter_id)

        if voterid_exists:
            print("ID successfully verified\n")

            # Retrieve the constituency for the given voter ID
            query_constituency = "SELECT constituency FROM voterinfo WHERE voter_id = %s"
            cur.execute(query_constituency, (voter_id,))
            constituencies = cur.fetchall()

            # For each retrieved constituency, display MPs
            for constituency in constituencies:
                constituency_name = constituency[0]
                print("** Vote for your preferred MP **")

                query_mps = "SELECT * FROM members_of_parliament WHERE constituency = %s"
                cur.execute(query_mps, (constituency_name,))
                mps = cur.fetchone()
                if mps:
                    count = -2
                    for mp in mps:
                        if mp is not None:
                            count += 1
                            if count > 0:
                                print(count, mp)
                else:
                    print(f"No MPs found for constituency {constituency_name}")

        else:
            print("Sorry, you have entered an invalid id. Try again")
    except Error as e:
        print(f"Database error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
