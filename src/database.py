import psycopg2
from logger import Logger


def create_database():
    conn = psycopg2.connect(dbname="neondb", user="EgorBa", password="TzsFvo7Qi4Uc", host="ep-falling-morning-557748.us-east-2.aws.neon.tech")
    cursor = conn.cursor()

    conn.autocommit = True
    sql = "CREATE TABLE IF NOT EXISTS penguins  (dat varchar)"

    cursor.execute(sql)
    logger = Logger(True)
    log = logger.get_logger("database")
    log.info("database was created")

    cursor.close()
    conn.close()