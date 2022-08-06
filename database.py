import os
import sqlite3
from sqlite3 import Error
import pandas as pd

pd.set_option('display.max_columns', None)  # or 1000
pd.set_option('display.max_rows', None)  # or 1000
pd.set_option('display.max_colwidth', None)  # or 199
pd.set_option('display.width', None)


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)


def create_table(table_name, customer_file, conn):
    df = pd.read_excel(customer_file, engine='openpyxl')
    df.to_sql(name=table_name, con=conn, if_exists='append')


def main():
    conn = create_connection(f'{os.getcwd()}/4g_capital.db')
    create_table('customer_affordability', 'affordability_training.xlsx', conn)
    conn.close()


if __name__ == '__main__':
    main()
