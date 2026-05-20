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

TABLE = """
        CREATE TABLE IF NOT EXISTS tasks( 
        task_id INT NOT NULL AUTO_INCREMENT,
        description VARCHAR(50) NOT NULL, 
        status VARCHAR(50) DEFAULT 'todo', 
        createdAt DATETIME DEFAULT NOW(),
        updatedAt DATETIME DEFAULT NOW(),
        PRIMARY KEY (task_id)
        )
    """

def connect_mysql_db():
    config = {"host":db_host,
            "port":db_port,
            "user":db_user,
            "password":db_password,
            "database":"task-tracker"}
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        print("Connected succesfully to database.")
        create_table(connection)
        return connection
    except mysql.connector.Error as err:
        print(err.msg)

def check_if_table_exists(connection, table_name):
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    for table in cursor:
        if table[0] == table_name:
            return True
    return False


def create_table(connection):
    cursor = connection.cursor()
    try:
        if check_if_table_exists(connection,"tasks"):
            print("Table Already Exists.")
        else:
            cursor.execute(TABLE)
            print(f"Creating tasks table.")
    except mysql.connector.Error as err:
        if err == errorcode.ER_TABLE_EXISTS_ERROR:
            pass
        else:
            print(f"Error from MySQL: {err.msg}")

def add_task(connection, description, status='todo'):
    params = (description, status)
    cursor = connection.cursor()
    query = """ INSERT INTO tasks (description,status)
                VALUES (%s,%s);
    """
    try:
        cursor.execute(query,params)
        connection.commit()
        print(f"Task '{description}' added to database.")
    except mysql.connector.Error as err:
        print(err.msg)

def update_task(connection, task_id, new_description):
    params = (new_description, task_id)
    cursor = connection.cursor()
    query = """ UPDATE tasks 
    SET description = %s, updatedAt = NOW() 
    WHERE task_id = %s;
    """
    try:
        cursor.execute(query,params)
        connection.commit()
        print(f'Task {task_id} changed to {new_description} sucessfully.')
    except mysql.connector.Error as err:
        print(f'Error updating task {task_id}: {err.msg}')

def delete_task(connection, task_id):
    cursor = connection.cursor()
    query = """DELETE FROM tasks
    WHERE task_id = %s
    """
    params = (task_id,)
    try:
        cursor.execute(query,params)
        connection.commit()
        print(f'Task {task_id} deleted succesfully.')
    except mysql.connector.Error as err:
        print(f'Error updating task {task_id}: {err.msg}')

def update_status_task(connection, task_id, new_status):
    params = (new_status, task_id)
    cursor = connection.cursor()
    query = """ UPDATE tasks 
    SET status = %s, updatedAt = NOW() 
    WHERE task_id = %s;
    """
    try:
        cursor.execute(query,params)
        connection.commit()
        print(f'Task {task_id} status changed to {new_status} sucessfully.')
    except mysql.connector.Error as err:
        print(f'Error updating task {task_id}: {err.msg}')

def list_tasks(connection, status):
    cursor = connection.cursor()
    params = (status,)
    query = """SELECT task_id, description
    FROM tasks 
    WHERE status = %s;
    """
    try:
        cursor.execute(query,params)
        resultados = cursor.fetchall()
        for resultado in resultados:
            print(f"{resultado[0]} - {resultado[1]}")
    except mysql.connector.Error as err:
         print(f'Error listing all tasks with status {status}: {err.msg}')

def list_all_tasks(connection):
    cursor = connection.cursor()
    query = """SELECT task_id, description
    FROM tasks;
    """
    try:
        cursor.execute(query)
        resultados = cursor.fetchall()
        for resultado in resultados:
            print(f"{resultado[0]} - {resultado[1]}")
    except mysql.connector.Error as err:
         print(f'Error listing all tasks: {err.msg}')