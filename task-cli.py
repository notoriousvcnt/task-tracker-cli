import argparse
import mysql_database
from simple_log import log
import simple_log


connection = mysql_database.connect_mysql_db()

# ---- ADD COMMANDS VIA PARSER AND SUBPARSERS ---- #
parser = argparse.ArgumentParser();
parser.add_argument("--debug","-d",action="store_true")
subparsers = parser.add_subparsers(dest="action")

#add
add_parser = subparsers.add_parser("add")
add_parser.add_argument("task_description")

#delete
delete_parser = subparsers.add_parser("delete")
delete_parser.add_argument("task_id")

#update
update_parser = subparsers.add_parser("update")
update_parser.add_argument("task_id")
update_parser.add_argument("new_task_description")

#mark-in-progress
in_progress_parser = subparsers.add_parser("mark-in-progress")
in_progress_parser.add_argument("task_id")

#mark-in-progress
done_parser = subparsers.add_parser("mark-done")
done_parser.add_argument("task_id")

#list
list_parser = subparsers.add_parser("list")
list_parser.add_argument("status",nargs="?")

# ------------------------------------------------

args = parser.parse_args()


# ----- AUXILIARY FUNCTIONS ---------------- #

def toDict(args):
    args_dict = vars(args)
    return args_dict

def print_dict(cli_args):
    args = vars(cli_args)
    for key in args:
        print(f'{key}: {args[key]}')

# ------------------------ ROUTER ------------- #
args_dict = toDict(args)

if args_dict["debug"] == True:
    simple_log.active = True

if args_dict["action"] == "add":
    task_description = args_dict["task_description"]
    log(f"adding task {task_description}")
    mysql_database.add_task(connection, task_description)
elif args_dict["action"] == "update":
    task_id = args_dict["task_id"]
    new_description = args_dict["new_task_description"]
    mysql_database.update_task(connection, task_id, new_description)
elif args_dict["action"] == "delete":
    task_id = args_dict["task_id"]
    log(f"deleting task {task_id}")
    mysql_database.delete_task(connection, task_id)
elif args_dict["action"] == "mark-in-progress":
    task_id = args_dict["task_id"]
    new_status = "in-progress"
    log(f"marking in progress task {task_id}")
    mysql_database.update_status_task(connection, task_id, new_status)
elif args_dict["action"] == "mark-done":
    task_id = args_dict["task_id"]
    new_status = "done"
    log(f"marking done task {task_id}")
    mysql_database.update_status_task(connection, task_id, new_status)
elif args_dict["action"] == "list":
    status = args_dict["status"]
    if  status == None:
        log("listing all tasks.")
        mysql_database.list_all_tasks(connection)
    elif status == "done":
        log("listing done tasks.")
        mysql_database.list_tasks(connection, status)
    elif status == "in-progress":
        log("listing in-progress tasks.")
        mysql_database.list_tasks(connection, status)
    elif status == "todo":
        log("listing pending tasks.")
        mysql_database.list_tasks(connection, status)
    else:
        print("not recognized argument for list command.")
else:
    print("command not recognized.")