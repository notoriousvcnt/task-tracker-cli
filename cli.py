
import argparse

commands = { "add": "add task",
            "update":"update task",
            "delete":"delete task",
            "mark-in-progress": "mark task in progress",
            "mark-done": "mark task done",
            "list": "list all tasks",
            "list done" : "list done tasks",
            "list todo": "list todo tasks",
            "list in-progress":"list in progress tasks"
            }

parser = argparse.ArgumentParser();

for key in commands:
    parser.add_argument(key,help=commands[key])

parser.parse_args()