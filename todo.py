#!/usr/bin/env python3
"""Simple To-Do CLI app.
Usage:
  python3 todo.py add "task description"
  python3 todo.py list
  python3 todo.py remove 1
Data is saved in data/tasks.json (relative to this script).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

# Storage paths (relative to this file so it works inside/outside Docker)
DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_FILE = DATA_DIR / "tasks.json"


def ensure_storage() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")


def load_tasks() -> list[dict]:
    ensure_storage()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # If file is corrupted, start fresh (or raise an error)
        return []


def save_tasks(tasks: list[dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


def add_task(description: str) -> None:
    tasks = load_tasks()
    next_id = (max((t.get("id", 0) for t in tasks), default=0) + 1)
    tasks.append({"id": next_id, "description": description})
    save_tasks(tasks)
    print(f"Added [{next_id}] {description}")


def list_tasks() -> None:
    tasks = load_tasks()
    if not tasks:
        print("No tasks.")
        return
    for t in tasks:
        print(f"[{t['id']}] {t['description']}")


def remove_task(task_id: int) -> None:
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t.get('id') != task_id]
    if len(new_tasks) == len(tasks):
        print(f"No task with id {task_id} found.")
        return
    save_tasks(new_tasks)
    print(f"Removed task {task_id}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Simple To-Do CLI.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help='Add a task: add "task description"')
    p_add.add_argument("description", nargs="+", help="Task description")
    p_add.set_defaults(func=lambda args: add_task(" ".join(args.description)))

    p_list = sub.add_parser("list", help="List all tasks")
    p_list.set_defaults(func=lambda args: list_tasks())

    p_remove = sub.add_parser("remove", help="Remove a task by ID")
    p_remove.add_argument("id", type=int, help="Task ID")
    p_remove.set_defaults(func=lambda args: remove_task(args.id))

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
