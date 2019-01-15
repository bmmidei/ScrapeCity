import sqlite3 as lite
from sqlite3 import Error

def create_connection(db):
    ''' Create db connection to local sqlite db 
    :param db_file: File system location of db
    :return: Connection object
    '''
    try:
        conn = lite.connect(db)
        return conn
    except Error as e:
        print(e)

    return None

def create_apt_table(conn):
    ''' Create the apartment sql table if it doesn't exist
    :param conn: Connection object
    :return: None 
    '''
    sql = '''CREATE TABLE IF NOT EXISTS apts(
                rentalkey text PRIMARY KEY,
                bldg_id text,
                min_rent integer,
                max_rent integer,
                beds text,
                baths text,
                min_area integer,
                max_area integer
                );'''
    # Context manager for executing sql
    with conn:
        try:
            c = conn.cursor()
            c.execute(sql)
        except Error as e:
            print(e)


def add_apt(conn, apt):
    """
    Add new apt to apts table
    :param conn: sql connection
    :param apts: apts dict
    :return: None
    """
    apt_info = (apt['rentalkey'],
                apt['bldg_id'],
                apt['min_rent'],
                apt['max_rent'],
                apt['beds'],
                apt['baths'],
                apt['min_area'],
                apt['max_area'])
    sql = ''' INSERT INTO apts(rentalkey, bldg_id, min_rent, max_rent, beds, baths, min_area, max_area)
              VALUES(?,?,?,?,?,?,?,?) '''

    # Context manager for executing sql
    with conn:
        try:
            c = conn.cursor()
            c.execute(sql, apt_info)
        except Error as e:
            print(e)

    return None

def create_bldg_table(conn):
    ''' Create the building metadata sql table if it doesn't exist
    :param conn: Connection object
    :return: None 
    '''
    sql = '''CREATE TABLE IF NOT EXISTS bldg_meta(
                bldg_id text PRIMARY KEY,
                name text,
                street text,
                city text,
                state text,
                zip text,
                nb_hood text
                );'''
    # Context manager for executing sql
    with conn:
        try:
            c = conn.cursor()
            c.execute(sql)
        except Error as e:
            print(e)

def add_bldg_meta(conn, bldg_meta):
    """
    Add new bldg to bldg table
    :param conn: sql connection
    :param bldg_meta: building metadata dict
    :return: None
    """
    bldg_info = (bldg_meta['bldg_id'],
                 bldg_meta['name'],
                 bldg_meta['street'],
                 bldg_meta['city'],
                 bldg_meta['state'],
                 bldg_meta['zip'],
                 bldg_meta['nb_hood'])
    sql = ''' INSERT INTO bldg_meta(bldg_id, name, street, city, state, zip, nb_hood)
              VALUES(?,?,?,?,?,?,?) '''

    # Context manager for executing sql
    with conn:
        try:
            c = conn.cursor()
            c.execute(sql, bldg_info)
        except Error as e:
            print(e)

    return None