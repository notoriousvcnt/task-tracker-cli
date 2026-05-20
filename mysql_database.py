import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv
from simple_log import log

#load .env
load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT") 
db_user = os.getenv("DB_USER") 
db_password = os.getenv("DB_PASSWORD") 

TABLE = """
        CREATE TABLE IF NOT EXISTS tasks( 
        task_id INT NOT NULL AUTO_INCREMENT,
        description VARCHAR(255) NOT NULL, 
        status ENUM('todo', 'in-progress', 'done') DEFAULT 'todo', 
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
        log("Connected succesfully to database.")
        create_table(connection)
        return connection
    except mysql.connector.Error as err:
        raise SystemExit(f"Could not connect to MySQL database: {err.msg}")


def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(TABLE)
    except mysql.connector.Error as err:
        log(f"Error from MySQL: {err.msg}")
       

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
        log(err.msg)

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
        if cursor.rowcount > 0:
            print(f'Task {task_id} changed to {new_description} sucessfully.')
        else:
            print(f"Task {task_id} not found.")
        
    except mysql.connector.Error as err:
        log(f'Error updating task {task_id}: {err.msg}')

def delete_task(connection, task_id):
    cursor = connection.cursor()
    query = """DELETE FROM tasks
    WHERE task_id = %s
    """
    params = (task_id,)
    try:
        cursor.execute(query,params)
        connection.commit()
        if cursor.rowcount > 0:
            print(f'Task {task_id} deleted succesfully.')
        else:
            print(f"Task {task_id} not found.")
    except mysql.connector.Error as err:
        log(f'Error updating task {task_id}: {err.msg}')

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
        if cursor.rowcount > 0:
            print(f'Task {task_id} status changed to {new_status} sucessfully.')
        else:
            print(f'Error chaning status to task {task_id}. Maybe it doesn\'t exists or status is incorrect.')
    except mysql.connector.Error as err:
        log(f'Error updating task {task_id}: {err.msg}')

def list_tasks(connection, status):
    cursor = connection.cursor()
    params = (status,)
    query = """SELECT task_id, description, status
    FROM tasks 
    WHERE status = %s;
    """
    try:
        cursor.execute(query,params)
        resultados = cursor.fetchall()
        for resultado in resultados:
            print(f"{resultado[0]} - {resultado[1]} - status: {resultado[2]}")
    except mysql.connector.Error as err:
        log(f'Error listing all tasks with status {status}: {err.msg}')

def list_all_tasks(connection):
    cursor = connection.cursor()
    query = """SELECT task_id, description, status
    FROM tasks;
    """
    try:
        cursor.execute(query)
        resultados = cursor.fetchall()
        for resultado in resultados:
            print(f"{resultado[0]} - {resultado[1]} - status: {resultado[2]}")
    except mysql.connector.Error as err:
         log(f'Error listing all tasks: {err.msg}')