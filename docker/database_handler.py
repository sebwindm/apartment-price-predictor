import psycopg2
from datetime import datetime


def open_connection():
    """
    Open a connection to the remote PostgreSQL database and return connection object
    :return: psycopg2 connection object
    """
    # If there are problems with the password, see https://www.liquidweb.com/kb/change-a-password-for-postgresql-on-linux-via-command-line/
    f = open("db_info.txt", "r")
    dbname = f.readline()
    username = f.readline()
    pw = f.readline()
    return psycopg2.connect("dbname="+ str(dbname) + "user=" + str(username) + "password=" + str(pw) +  "host=78.47.75.121")

def insert_offerings(offering_list):
    """
    Take a dictionary as argument and
    :param offering_list: dictionary. Must be in the structure of webscraper.py -> list_of_all_offer_data
    :return: error (string) contains the potential error message from PostgreSQL
    """
    conn = open_connection()
    error = None
    try:
        # create a cursor
        cur = conn.cursor()
        # Insert content of offer_list into database
        cur.executemany("""INSERT INTO offerings(offering_id, access_date, rent, living_space, number_rooms) 
        VALUES (%(offering_id)s, %(access_date)s ,%(rent)s,%(living_space)s,%(number_rooms)s)""", offering_list)
        # commit the changes to the database
        conn.commit()
        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

    return error

def fully_reset_database_table():
    """
    Delete table 'offerings' and create a new one
    (resets primary key 'entry_id' instead of just truncating)
    :return:
    """
    conn = open_connection()
    try:
        # create a cursor
        cur = conn.cursor()

        cur.execute("""DROP TABLE offerings""")

        cur.execute("""CREATE TABLE offerings(
        entry_id serial PRIMARY KEY,
        offering_id INTEGER NOT NULL,
        access_date DATE NOT NULL,
        rent decimal NOT NULL,
        living_space decimal NOT NULL,
        number_rooms decimal NOT NULL
        );
        """)

        # commit the changes to the database
        conn.commit()

        # close the communication with the PostgreSQL
        cur.close()
        was_successful = True

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        was_successful = False

    finally:
        if conn is not None:
            conn.close()

    return

def get_statistics():
    conn = open_connection()
    cur = conn.cursor()

    cur.execute("""SELECT COUNT(entry_id)
    FROM offerings;""")
    info = cur.fetchone()
    cur.close()
    if conn is not None:
        conn.close()
    return info

def remove_duplicates():
    """
    Remove all rows where 'offering_id' is identical, but keep the oldest one (with lowest 'entry_id').
    :return: number_of_rows_with_duplicates, duplicates_after_deletion, error
    number_of_rows_with_duplicates: integer. Number of rows which have a duplicate 'offering_id' somewhere in the
                                    table 'offerings'. Note that this counts all rows, so if the result is 1400,
                                    there are 700 originals and 700 duplicates
    duplicates_after_deletion: same as number_of_rows_with_duplicates, this is just to verify that the duplicate
                                deletion process has worked
    error: string. Any potential error messages received from PostgreSQL
    """
    conn = open_connection()
    number_of_rows_with_duplicates = None
    duplicates_after_deletion = None
    error = None
    try:
        # create a cursor
        cur = conn.cursor()

        # Check how many rows have duplicate values
        cur.execute("""select * from offerings t1
        where exists
        (select 1 from offerings t2
        where t1.offering_id = t2.offering_id and t1.entry_id <> t2.entry_id)
        ;""")
        number_of_rows_with_duplicates = len(cur.fetchall())

        # Delete newer entry_ids from rows with duplicates
        cur.execute("""
        delete FROM offerings a
        USING offerings b
        WHERE
        a.entry_id < b.entry_id
        AND a.offering_id = b.offering_id;
        """)
        # Check how many rows have duplicate values after deletion
        cur.execute("""select * from offerings t1
        where exists
        (select 1 from offerings t2
        where t1.offering_id = t2.offering_id and t1.entry_id <> t2.entry_id)
        ;""")
        duplicates_after_deletion = len(cur.fetchall())

        # close the communication with the PostgreSQL
        cur.close()

        # commit the changes to the database
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()

    return number_of_rows_with_duplicates, duplicates_after_deletion, error


if __name__ == '__main__':
    print(get_statistics())






