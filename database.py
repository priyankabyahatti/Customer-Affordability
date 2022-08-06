""" This Script creates a database and a table within it to store customer affordability data. This
script is run the first time """

import os
import sqlite3
from sqlite3 import Error
import pandas as pd


def create_connection(db_file):
    """ This function creates a database connection to a SQLite database
    Args:
        db_file: path to save database """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)


def create_table(table_name, customer_file, conn) -> None:
    """ This function creates a table with 4g capital database and loads affordability data
    Args:
        table_name: name of the table to store affordability data
        customer_file: data file (excel)
        conn: database connection sqlite
    """
    df = pd.read_excel(customer_file, engine='openpyxl')
    df.to_sql(name=table_name, con=conn, if_exists='append')


def main():
    """ This function creates connection to db, creates table to save data and closes the db connection """
    conn = create_connection(f'{os.getcwd()}/4g_capital.db')
    create_table('customer_affordability', 'affordability_training.xlsx', conn)
    conn.close()


if __name__ == '__main__':
    main()