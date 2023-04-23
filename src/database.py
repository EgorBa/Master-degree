import psycopg2
import pandas as pd
from pandas import DataFrame
from config import *

from logger import Logger

SHOW_LOG = True
TAG = "Database"


class DataBase:

    def __init__(self) -> None:
        logger = Logger(SHOW_LOG)
        self.log = logger.get_logger(__name__)
        self.project_path = os.path.join(os.getcwd(), "data")
        self.data_path = os.path.join(self.project_path, "penguins_size.csv")
        self.create_database()
        self.add_data_from_path()

    def create_database(self):
        self.log.info(f"table \"{DATABASE_NAME}\" creating start")

        conn = psycopg2.connect(dbname=DATABASE_N, user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST)
        cursor = conn.cursor()

        conn.autocommit = True

        sql = F"DROP TABLE IF EXISTS {DATABASE_NAME};"
        cursor.execute(sql)

        sql = F"CREATE TABLE {DATABASE_NAME} ({DATABASE_COLUMN} varchar)"
        cursor.execute(sql)

        self.log.info(f"table \"{DATABASE_NAME}\" was created")

        cursor.close()
        conn.close()

    def add_data_from_path(self):
        dataset = pd.read_csv(self.data_path)
        all_data = []
        for i in range(len(dataset)):
            data_str = ""
            for j in range(len(dataset.loc[i])):
                data_str += str(dataset.loc[i][j])
                if j != len(dataset.loc[i]) - 1:
                    data_str += ","
            all_data.append(data_str)
        self.add_lines(all_data)

    def add_line(self, line):
        conn = psycopg2.connect(dbname=DATABASE_N, user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST)
        cursor = conn.cursor()

        conn.autocommit = True

        line_data = f"(\'{line}\')"
        sql = f"INSERT INTO {DATABASE_NAME}({DATABASE_COLUMN}) VALUES {line_data}"
        cursor.execute(sql)

        self.log.info(f"data was added {line}")

        cursor.close()
        conn.close()

    def add_lines(self, lines):
        conn = psycopg2.connect(dbname=DATABASE_N, user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST)
        cursor = conn.cursor()

        conn.autocommit = True
        line_data = ""
        for i, line in enumerate(lines):
            line_data += f"(\'{line}\')"
            if i != len(lines) - 1:
                line_data += ","
        sql = f"INSERT INTO {DATABASE_NAME}({DATABASE_COLUMN}) VALUES {line_data}"
        cursor.execute(sql)

        self.log.info(f"data was added {lines}")

        cursor.close()
        conn.close()

    def get_data_as_dataframe(self) -> DataFrame:
        conn = psycopg2.connect(dbname=DATABASE_N, user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST)
        cursor = conn.cursor()

        conn.autocommit = True
        sql = f"SELECT * FROM {DATABASE_NAME}"
        cursor.execute(sql)

        all_data = []
        for dat in cursor.fetchall():
            data = dat[0].split(",")
            list_data = []
            for i in range(len(data)):
                list_data.append(data[i])
            all_data.append(list_data)
        df = pd.DataFrame(all_data,
                          columns=['species', 'island', 'culmen_length_mm', 'culmen_depth_mm', 'flipper_length_mm',
                                   'body_mass_g', 'sex'])
        self.log.info(f"data was got {df}")

        cursor.close()
        conn.close()
        return df
