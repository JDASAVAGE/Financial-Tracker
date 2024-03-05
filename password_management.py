import mysql.connector
from mysql.connector import Error
import pandas as pd
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def execute_query_data_adding(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result=connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def execute_query_data_retreieving(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result=cursor.fetchall()
        print("Query successful")
        return result
    except Error as err:
        print(f"Error: '{err}'")


