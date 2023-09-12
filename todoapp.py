#! /bin/python3

import pickle
from os import path
from sys import stderr, stdout
from datetime import datetime
import argparse
from argparse import Namespace

class Task:
    def __init__(
        self,
        title:str,
        desc: str = None,
        due: datetime = None,
        priority: int = None
    ):
        self.title = title
        self.description = desc
        self.created = datetime.now()
        self.due = due if due else None
        self.priority = priority if priority else 0

class Tasklist:
    def __init__(self):
        self.tasks = self.load_data()

    def remove_task(self, args:Namespace):
        id = args.id
        if id > len(self.tasks):
            print(f"Task #{id} doesn't exists", file=stdout)
            return
        task = self.tasks[id]
        self.tasks.remove(task)
        self.list_tasks()
        self.save_data()

    def purge_tasks(self, args:any = None):
        self.tasks = []
        self.save_data()
        self.list_tasks()

    def list_tasks(self, args:Namespace | None = None):
        if len(self.tasks) < 1:
            print("Nothig in the list yet. You can start adding tasks!", file=stdout)
        for id, task in enumerate(self.tasks):
            print(
                    id,
                    ': ',
                    task.title,
                    # task.description,
                    # task.due,
                    # task.priority,
                    file=stdout
            )

    def add_task(self, args:Namespace) -> None:
        self.tasks.append(
            Task(
                ' '.join(args.title),
                ' '.join(args.description) if args.description else None,
                args.date if args.date else None,
                args.priority if args.priority else None
            )
        )

        self.save_data()
        self.list_tasks(args)

    def load_data(self, filename:str = "jar"):
        data  = []
        if path.isfile(filename):
            try:
                with open(filename, "rb") as file:
                    data = pickle.load(file)
            except Exception as e:
                print(e, file=stderr)

        return data

    def save_data(self, filename:str="jar") -> None:
        try:
            with open(filename, "wb") as file:
                pickle.dump(self.tasks, file)
        except Exception as e:
            print(e, file=stderr)








def main():

    tasks = Tasklist()


    parser = argparse.ArgumentParser()


    subparsers = parser.add_subparsers(
        help="Tools for working with a list"
    )

    parser_add = subparsers.add_parser(
        "add",
        help="Adds new task into the list"
    )

    parser_add.add_argument(
        "title",
        type=str,
        nargs="*"
    )

    parser_add.add_argument(
        "-d",
        "--date",
        help="Due date if DD.MM.YYYY format"
    )

    parser_add.add_argument(
        "-e",
        "--description",
        type=str,
        nargs="*"
    )

    parser_add.add_argument(
        "-p",
        "--priority",
        type=int,
        default=0,
        help="Priority of the task. Value 0 for normal and 1 for important"
    )

    parser_add.set_defaults(func=tasks.add_task)

    parser_list = subparsers.add_parser(
        "list",
        help="Lists all the tasks"
    )

    parser_list.add_argument(
        "-n",
        "--name",
        const="tasks",
        action="store_const",
        dest="params"
    )

    parser_list.set_defaults(func=tasks.list_tasks)

    parser_remove = subparsers.add_parser(
        "remove",
        help="Removes a task from the list"
    )
    parser_remove.add_argument("id", type=int)
    parser_remove.set_defaults(func=tasks.remove_task)
    parser_purge = subparsers.add_parser("purge", help="Clears the list")
    parser_purge.set_defaults(func=tasks.purge_tasks)



    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)

    else:
        tasks.list_tasks(args)











if  __name__ == "__main__":
    main()
