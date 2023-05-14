import random
import tkinter as tk
import os
import sys


def draw_student_number(min_number, max_number):
    return random.randint(min_number, max_number)


def update_label():
    min_number = int(min_entry.get())
    max_number = int(max_entry.get())
    drawn_number = draw_student_number(min_number, max_number)
    label.config(text=f"被抽中的学号是: {drawn_number}")


def save_range():
    min_number = min_entry.get()
    max_number = max_entry.get()
    with open('range.txt', 'w') as f:
        f.write(f"{min_number}\n{max_number}")
    root.destroy()
    os.execl(sys.executable, sys.executable, *sys.argv)


def load_range():
    if os.path.exists('range.txt'):
        with open('range.txt', 'r') as f:
            min_number, max_number = f.read().splitlines()
            min_entry.delete(0, tk.END)
            min_entry.insert(0, min_number)
            max_entry.delete(0, tk.END)
            max_entry.insert(0, max_number)


def open_range_window():
    root.attributes('-topmost', False)
    range_window = tk.Toplevel(root)
    range_window.title("修改学号范围")
    range_window.grab_set()

    label = tk.Label(range_window, text="最小学号: ")
    label.pack()

    global min_entry
    min_entry = tk.Entry(range_window)
    min_entry.pack()

    label = tk.Label(range_window, text="最大学号: ")
    label.pack()

    global max_entry
    max_entry = tk.Entry(range_window)
    max_entry.pack()

    button = tk.Button(range_window, text="保存范围", command=save_range)
    button.pack()


root = tk.Tk()
root.title("抽取学号")
root.attributes('-topmost', True)

label = tk.Label(root, text="被抽中的学号是: ")
label.pack()

button = tk.Button(root, text="抽取学号", command=update_label)
button.pack()

button = tk.Button(root, text="修改学号范围", command=open_range_window)
button.pack()

min_entry = tk.Entry(root)
max_entry = tk.Entry(root)

load_range()

root.mainloop()
