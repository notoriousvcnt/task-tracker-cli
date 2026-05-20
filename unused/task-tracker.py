# Functions related to handle tasks
from enum import Enum

class TaskStatus(Enum):
    TODO = 1
    IN_PROGRESS = 2
    DONE = 3


def add_task(task):
    return

def update_task(id_task,new_description):
    return 

def delete_task(id_task):
    return
    
def update_status_task(id_task,status):
    return

def list_tasks(status_filter=None):
    match status_filter:
        case TaskStatus.DONE:
            print("Tareas terminadas")
        case TaskStatus.TODO:
            print("Tareas pendientes")
        case TaskStatus.IN_PROGRESS:
            print("Tareas en progreso")
        case None:
            print("mostrando todas las tareas")
        case _:
            print("No válido")
            
