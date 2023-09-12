#! /bin/python3

import pickle
from os import path
from sys import stderr, stdout
from datetime import datetime
import argparse

class Task:
    def __init__(self,
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
        self.tasks = []

    def get_tasks(self) -> [Task]:
        return self.tasks

    def get_sorted(self, key:str) -> [Task]:
        ...

    def add_task(self, task:Task) -> None:
        self.tasks.append(task)



def main():

    tasks = []

    if path.isfile("jar"):
        try:
            with open("jar", "rb") as file:
                tasks = pickle.load(file)
        except EOFError as e:
            print("e", file=stderr)

    parser = argparse.ArgumentParser()

    parser.add_argument("title", type=str, nargs="*")
    parser.add_argument("-d", "--date", help="Due date if DD.MM.YYYY format")
    parser.add_argument("-e", "--description", type=str, nargs="*")
    parser.add_argument("-p", "--priority", type=int, default=0, help="Priority of the task. Value 0 for normal and 1 for important")

    args = parser.parse_args()

    if args.title:

        tasks.append(Task(
            ' '.join(args.title),
            ' '.join(args.description) if args.description else None,
            args.date if args.date else None,
            args.priority if args.priority else None
            ))

        try:
            with open("jar", "wb") as file:
                pickle.dump(tasks, file)
        except Exception as e:
            print(e, file=stderr)

    else:

        for id, task in enumerate(tasks):
            print(id, ' : ', task.title, task.description, task.due, task.priority )



if  __name__ == "__main__":
    main()
