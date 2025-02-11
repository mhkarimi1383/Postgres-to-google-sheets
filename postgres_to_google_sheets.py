import psycopg2
import pandas as pd
import pygsheets
from psycopg2 import Error
from connection import connection
from config import config
import os
import json


def table_to_sheets(query, sheet_name):
    # Connect to the PostgreSQL database server
    conn = None
    try:
        # read connection parameters
        params = connection()

        print (params)

        # connect to the PostgreSQL server
        print('connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        config_data = config()
        # get config info

        credential_file_name = config_data['credential_file_name']

        # Using pandas library, get the data from the table as a dataFrame
        df = pd.read_sql('{query}'.format(query=query), conn)
        #print(df)
        print('successfully read in data')

        # get working directory path
        dirpath = os.getcwd()
        credential_file_location = dirpath + '/' +credential_file_name
        #print(credential_file_location)

        # authorise connection to your google sheets
        gc = pygsheets.authorize(service_file = credential_file_location)
        print('successfully authorised and connected to google sheets')

        # open the google spreadsheet with the provided sheet name
        sh = gc.open_by_key(sheet_name)
        print('opened the sheet with the sheet name provided as ' + sheet_name)

        # select the first sheet as the worksheet
        wks = sh.sheet1

        # clear the worksheet
        wks.clear(start='A1', end=None, fields='*')
        print('worksheet has been cleared')

        # update the first sheet with the dataFrame df, starting at cell B2.
        wks.set_dataframe(df,(1,1))
        print('data from the database table has been transferred to the google spreadsheet')

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('database connection closed')

#if __name__ == '__main__':
    # table_to_sheets(query, sheet_name)


