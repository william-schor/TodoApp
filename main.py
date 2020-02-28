# -*- coding: utf-8 -*-

"""Module Summary

Additional details...

Functions
-----------
f(str, int): finds the int in the str and returns the index
"""

import os
import sys
import pickle
import json
import argparse

MY_LOCATION = os.path.dirname(os.path.abspath(__file__))

HISTORY_PATH = f"{MY_LOCATION}/history.pkl"
DONE_PATH = f"{MY_LOCATION}/done_list.pkl"
TODO_PATH = f"{MY_LOCATION}/todo_list.pkl"


class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    STRIKE = "\u0336"
    END = "\033[0m"


def _del_(number, path):
    items = _read_(path)
    if type(number) != int or number < 1 or number > len(items):
        print("Invalid ID! Options are:")
        output(items, "TODO", color.BOLD)
        return

    confirm = items[number - 1]
    yes = input(f"\n{color.BOLD}remove {confirm}{color.END}? [Y/n]: ")
    if "y" in yes.lower():

        del items[number - 1]

        if path == TODO_PATH:
            _append_(confirm, DONE_PATH)
            _write_(items, path)
            output(items, "TODO", color.RED)
            output(_read_(DONE_PATH), "DONE", color.GREEN)

        if path == DONE_PATH:
            _append_(confirm, HISTORY_PATH)
            _write_(items, path)
            print(f"\n{color.BOLD}Item archived{color.END}\n")


def _read_(path):
    todos = []
    with open(path, "rb") as f:
        while True:
            try:
                todos.append(pickle.load(f))
            except EOFError:
                break
    return todos


def _append_(content, path):
    if type(content) != list:
        content = [content]
    with open(path, "ab") as fp:
        for c in content:
            pickle.dump(c, fp)


def _write_(content, path):
    if type(content) != list:
        content = [content]
    with open(path, "wb") as fp:
        for c in content:
            pickle.dump(c, fp)


def output(todos, title, style):
    print(
        f"\n\t\t {color.BOLD} {title} \n----------------------------------------{color.END}"
    )
    for i, todo in enumerate(todos):
        print(f"{style}[{i+1}] {todo}{color.END}")
    print(f"{color.BOLD}---------------------------------------- {color.END}\n\n")


def main(args):

    if len(args) == 1:
        output(_read_(TODO_PATH), "TODO", color.RED)
        return

    parser = argparse.ArgumentParser(description="TODO app")
    parser.add_argument("-a", "--add", help="add a TODO item", required=False)
    parser.add_argument(
        "-d", "--done", type=int, help="mark a TODO item done by ID", required=False
    )
    parser.add_argument(
        "--archive",
        type=int,
        help='archive a completed item by ID (give "all" to archive all)',
        required=False,
    )
    parser.add_argument(
        "--history", "-hist", action="store_true", help="view history", required=False
    )
    parser.add_argument(
        "--completed",
        "-comp",
        action="store_true",
        help="view completed items",
        required=False,
    )

    args = vars(parser.parse_args())

    if args["add"]:
        _append_(args["add"], TODO_PATH)
        output(_read_(TODO_PATH), "TODO", color.RED)
        return

    if args["done"]:
        _del_(args["done"], TODO_PATH)
        return

    if args["archive"]:
        _del_(args["archive"], DONE_PATH)
        return

    if args["history"]:
        output(_read_(HISTORY_PATH), "HIST", color.BLUE)
        return

    if args["completed"]:
        output(_read_(DONE_PATH), "DONE", color.BLUE)
        return


if __name__ == "__main__":
    sys.exit(main(sys.argv))
