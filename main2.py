import threading
import random
import tkinter as tk
import tkinter.messagebox
import os
import sys
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import scrolledtext
import time

x = None
y = None


def get_student_number(min_number, max_number):
    return random.randint(min_number, max_number)


def update_label():
    min_number = int(min_entry.get())
    max_number = int(max_entry.get())

    # 清空滚动文本框内容
    scroll_text.delete(1.0, tk.END)

    t = threading.Thread(target=draw_numbers, args=(min_number, max_number))
    t.start()


def save_range():
    min_number = min_entry.get()
    max_number = max_entry.get()
    with open('./ranges/range.txt', 'w') as f:
        f.write(f"{min_number}\n{max_number}\n{initial_x}\n{initial_y}")
    os.execl(sys.executable, sys.executable, *sys.argv)


def load_range():
    global initial_x, initial_y
    if os.path.exists('./ranges/range.txt'):
        try:
            with open('./ranges/range.txt', 'r') as f:
                min_number, max_number, initial_x, initial_y = f.read().splitlines()
                min_entry.delete(0, tk.END)
                min_entry.insert(0, min_number)
                max_entry.delete(0, tk.END)
                max_entry.insert(0, max_number)
            initial_x = int(initial_x)
            initial_y = int(initial_y)
        except:
            with open('./ranges/range.txt', 'r') as f:
                min_number, max_number = f.read().splitlines()
                max_entry.delete(0, tk.END)
                max_entry.insert(0, max_number)
                max_entry.delete(0, tk.END)
                max_entry.insert(0, max_number)
            initial_x = 0
            initial_y = 0
            save_range()

    else:
        result = tk.messagebox.askyesno("初始化学号范围", "系统检测到您没有初始化学号范围，请设置后再抽学号")
        if result:
            open_range_window()
        else:
            root.destroy()


def open_range_window():
    global range_window
    root.attributes('-topmost', False)
    range_window = tk.Toplevel(root)
    range_window.title("修改学号范围")
    range_window.grab_set()
    range_window.iconbitmap('./ico.ico')

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

    button = ttk.Button(range_window, text="保存范围", command=save_range)
    button.pack()


initial_x = 0
initial_y = 0


def create_float_window():
    global initial_x, initial_y
    float_window = tk.Toplevel(root)
    float_window.geometry(f"130x40+{initial_x}+{initial_y}")
    float_window.overrideredirect(True)
    float_window.attributes('-topmost', True)

    button = ttk.Button(float_window, text="显示抽学号程序", command=lambda: show_main_window(float_window))
    button.pack(fill=tk.BOTH, expand=True)

    # Make the window draggable
    float_window.bind("<ButtonPress-1>", lambda event: start_move(event, float_window))
    float_window.bind("<ButtonRelease-1>", lambda event: stop_move(event, float_window))
    float_window.bind("<B1-Motion>", lambda event: do_move(event, float_window))
    root.withdraw()


def has_moved(float_window):
    return float_window.winfo_x() != initial_x or float_window.winfo_y() != initial_y


def show_main_window(float_window):
    if not has_moved(float_window):
        root.deiconify()
        float_window.destroy()


def start_move(event, float_window):
    global x, y
    x = event.x
    y = event.y


def stop_move(event, float_window):
    global x, y
    x = None
    y = None
    global initial_x, initial_y
    initial_x = float_window.winfo_x()
    initial_y = float_window.winfo_y()


def do_move(event, float_window):
    deltax = event.x - x
    deltay = event.y - y
    x_ = float_window.winfo_x() + deltax
    y_ = float_window.winfo_y() + deltay
    float_window.geometry(f"+{x_}+{y_}")


def draw_numbers(min_number, max_number):
    b = get_student_number(min_number, max_number)
    for i in range(b - min_number):
        label.config(text=f"学号滚动区显示为{i+min_number}")
        scroll_text.insert(tk.END, f"当前学号是: {i+min_number}\n")
        scroll_text.see(tk.END)
        root.update()
        c = b - min_number - i
        e = c / (b - min_number)
        time.sleep(0.05/e)


tem = ["superhero", "vapor", "cyborg", "solar", "cosmo", "flatly", "journal", "litera", "minty", "pulse", "morph"]
root = ttk.Window(themename=tem[random.randint(0, 10)])
root.title("抽取学号")
root.attributes('-topmost', True)
root.iconbitmap('./ico.ico')

label = tk.Label(root, text="被抽中的学号是: ")
label.pack()

button = ttk.Button(root, text="抽取学号", command=update_label, bootstyle="outline", width=30)
button.pack()

button = ttk.Button(root, text="点击缩小窗口", command=create_float_window, bootstyle="outline", width=30)
button.pack()

button = ttk.Button(root, text="修改学号范围", command=open_range_window, bootstyle="outline", width=30)
button.pack()

min_entry = tk.Entry(root)
max_entry = tk.Entry(root)

scroll_text = scrolledtext.ScrolledText(root, height=5, width=30)
scroll_text.pack()

load_range()

credit_label = tk.Label(root, text="程序制作by：小於菟工作室、刘贞", font=("KaiTi", 12), anchor='se')
credit_label.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()
