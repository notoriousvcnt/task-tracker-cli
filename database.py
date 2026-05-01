import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv

#load .env
load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT") 
db_user = os.getenv("DB_USER") 
db_password = os.getenv("DB_PASSWORD") 

config = {"host":db_host,
          "port":db_port,
          "user":db_user,
          "password":db_password,
          "database":"task-tracker"}

connection = mysql.connector.connect(**config)
cursor = connection.cursor()



TABLE = """
    CREATE TABLE tasks( 
       task_id INT NOT NULL AUTO_INCREMENT,
       description VARCHAR(50) NOT NULL, 
       status VARCHAR(50) DEFAULT 'todo', 
       createdAt DATETIME DEFAULT NOW(),
       updatedAt DATETIME DEFAULT NOW(),
       PRIMARY KEY (task_id)
       )
"""

def create_table(cursor):
    try:
        print("Creating tasks table: ",end="")
        cursor.execute(TABLE)
    except mysql.connector.Error as err:
        if err == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Table already exists.")
        else:
            print(err.msg)

create_table(cursor)