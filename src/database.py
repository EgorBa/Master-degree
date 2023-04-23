import psycopg2
from logger import Logger


def create_database():
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="12345678", host="127.0.0.1")
    cursor = conn.cursor()

    conn.autocommit = True
    sql = "CREATE DATABASE initdata"

    cursor.execute(sql)
    logger = Logger(True)
    log = logger.get_logger("database")
    log.info("database was created")

    cursor.close()
    conn.close()
