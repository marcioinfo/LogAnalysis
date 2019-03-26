import psycopg2
import logging

dbname = "news"


def ps_connection():
    try:
        logging.debug('Connecting to news DB')
        db = psycopg2.connect(database=dbname)
        conn = db.cursor()
        return conn
    except (psycopg2.Error, psycopg2.DatabaseError) as error:
        print(error)
