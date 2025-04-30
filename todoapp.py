import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import date
import json
import os

FILENAME = "tasks.json"

# 保存してあるタスクを読み込む
def load_tasks():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []

# タスクを保存する
def save_tasks(tasks):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ToDoアプリ")
        self.tasks = load_tasks()

        tk.Label(root, text="タスク:").pack(anchor="w", padx=10)
        self.entry = tk.Entry(root, width=40)
        self.entry.pack(pady=5)

        tk.Label(root, text="期日を入力 (例: 2025-04-30):").pack(anchor="w", padx=10)
        self.due_entry = DateEntry(root, width=20, date_pattern='yyyy-mm-dd', year=date.today().year, month=date.today().month, day=date.today().day)
        self.due_entry.pack(pady=5)

        self.add_button = tk.Button(root, text="タスク追加", command=self.add_task)
        self.add_button.pack(padx=5)

        self.listbox = tk.Listbox(root, width=50, selectmode=tk.SINGLE)
        self.listbox.pack(pady=5)

        self.done_button = tk.Button(root, text="完了済/未完了", command=self.mark_done)
        self.done_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="削除", command=self.delete_task)
        self.delete_button.pack(pady=5)

        self.update_listbox()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # タスクリストを表示させている
    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for t in self.tasks:
            mark = "✔" if t["done"] else "✖"
            due = f" (期日: {t['due']})" if t.get("due") else ""
            self.listbox.insert(tk.END, f"[{mark}] {t['task']}{due}")

    # タスクを追加する
    def add_task(self):
        task = self.entry.get().strip()
        due = self.due_entry.get().strip()
        if task:
            self.tasks.append({"task": task, "done": False, "due": due})
            self.entry.delete(0, tk.END)
            self.update_listbox()
    
    # タスクを削除する
    def delete_task(self):
        index = self.listbox.curselection()
        if index:
            del self.tasks[index[0]]
            self.update_listbox()
    
    # タスクを完了済/未完了にする
    def mark_done(self):
        index = self.listbox.curselection()
        # タスクを選んでいない場合はなにもしない（indexエラー対策）
        if not index:
            return
        
        # タスクを完了済みにする
        if self.tasks[index[0]]["done"] == False:
            self.tasks[index[0]]["done"] = True
            self.update_listbox()
        # タスクを未完了にする
        else:
            self.tasks[index[0]]["done"] = False
            self.update_listbox()

    # ウインドウを閉じる
    def on_close(self):
        save_tasks(self.tasks)
        self.root.destroy()

# アプリ起動時にmain()を実行させる記述
if __name__=="__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

