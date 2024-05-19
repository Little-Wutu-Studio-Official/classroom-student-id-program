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
import pickle
from ttkbootstrap import Style

x = None
y = None


def contains_all_numbers_between(lst, start, end):
    expected_numbers = set(range(start, end + 1))
    list_set = set(lst)
    return expected_numbers.issubset(list_set)


def draw_student_number(min_number, max_number):
    if checkbutton_var.get():
        while True:
            a = random.randint(min_number, max_number)
            if a in elselist and not contains_all_numbers_between(elselist, min_number, max_number):
                pass
            elif contains_all_numbers_between(elselist, min_number, max_number):
                elselist.clear()
                tkinter.messagebox.showinfo("信息", "该抽取项目内所有人都已经被抽取过了，即将自动重置……")
                else_files[combobox2.get()] = elselist
                print(else_files)
                save_else()
            else:
                elselist.append(a)
                print(elselist)
                else_files[combobox2.get()] = elselist
                print(else_files)
                save_else()
                return a
    else:
        return random.randint(min_number, max_number)


def update_label():
    min_number = int(min_entry.get())
    max_number = int(max_entry.get())

    scroll_text.delete(1.0, tk.END)

    t = threading.Thread(target=draw_numbers, args=(min_number, max_number))
    t.start()


def update_label1():
    min_number = int(min_entry.get())
    max_number = int(max_entry.get())
    drawn_number = draw_student_number(min_number, max_number)
    label.config(text=f"被抽中的学号是: {drawn_number}")


def save_range():
    x = False
    if else_files != {}:
        result = tk.messagebox.askyesno("保存？", "请注意，如果修改了学号范围，您的抽取项目将清空！")
        if result:
            os.remove('./ranges/else.pickle')
            try:
                min_number = int(min_entry.get())
                max_number = int(max_entry.get())
                if min_number >= max_number:
                    tkinter.messagebox.showerror("错误", "您输入的最小学号大于或等于最大学号！请重新输入。")
                    x = True
            except:
                tkinter.messagebox.showerror("错误", "您输入的学号范围不是整数！请重新输入。")
                x = True
            if not x:
                try:
                    with open('./ranges/range.txt', 'w') as f:
                        f.write(f"{min_number}\n{max_number}\n{initial_x}\n{initial_y}")
                    range_window.destroy()
                    os.execl(sys.executable, sys.executable, *sys.argv)
                except:
                    tkinter.messagebox.showerror("错误", "程序写入范围失败，请重新安装并不要改变预置路径！")
            else:
                pass
        else:
            pass
    else:
        try:
            min_number = int(min_entry.get())
            max_number = int(max_entry.get())
            if min_number >= max_number:
                tkinter.messagebox.showerror("错误", "您输入的最小学号大于或等于最大学号！请重新输入。")
                x = True
        except:
            tkinter.messagebox.showerror("错误", "您输入的学号范围不是整数！请重新输入。")
            x = True
        if not x:
            try:
                with open('./ranges/range.txt', 'w') as f:
                    f.write(f"{min_number}\n{max_number}\n{initial_x}\n{initial_y}")
                range_window.destroy()
                os.execl(sys.executable, sys.executable, *sys.argv)
            except:
                tkinter.messagebox.showerror("错误", "程序写入范围失败，请重新安装并不要改变预置路径！")
        else:
            pass



def new_else_list():
    name = name_else.get()
    if name in else_files:
        tkinter.messagebox.showerror("错误", "您输入了一个已经存在的名称，请重新输入")
    else:
        else_files[name] = []
        with open('./ranges/else.pickle', 'wb') as f:
            pickle.dump(else_files, f)
        else_window.destroy()
        tk.messagebox.askyesno("增加新的项目", "为了使得更改生效，请手动重启程序。")


def save_else():
    with open('./ranges/else.pickle', 'wb') as f:
        pickle.dump(else_files, f)


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

    else:
        result = tk.messagebox.askyesno("初始化学号范围", "系统检测到您没有初始化学号范围，请设置后再抽学号")
        if result:
            open_range_window()
        else:
            os.execl(sys.executable, *sys.argv)


def load_else():
    global else_files, keys_list
    if os.path.exists('./ranges/else.pickle'):
        with open('./ranges/else.pickle', 'rb') as f:
            else_files = pickle.load(f)
    else:
        else_files = {}
        with open('./ranges/else.pickle', 'wb') as f:
            pickle.dump(else_files, f)
    keys_list = list(else_files.keys())


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


def open_else_window():
    global else_window
    root.attributes('-topmost', False)
    else_window = tk.Toplevel(root)
    else_window.title("创建一个新的抽取项目")
    else_window.grab_set()
    else_window.iconbitmap('./ico.ico')

    label = tk.Label(else_window, text="请输入名称")
    label.pack()

    global name_else
    name_else = tk.Entry(else_window)
    name_else.pack()

    button = ttk.Button(else_window, text="创建", command=new_else_list)
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
    b = draw_student_number(min_number, max_number)
    for i in range(b - min_number + 1):
        label.config(text=f"学号滚动区显示为{i + min_number}")
        scroll_text.insert(tk.END, f"当前学号是: {i + min_number}\n")
        scroll_text.see(tk.END)
        root.update()
        c = b - min_number - i
        e = c / (b - min_number)
        if e != 0:
            time.sleep(0.05 / e)


def on_mode_change(event):
    selected_mode = mode_combobox1.get()
    MS1.set(selected_mode)
    if selected_mode == "炫酷可视模式":
        try:
            buttona.pack_forget()
            buttonb.pack_forget()
        except:
            pass
        label.pack()
        button_get_ps.pack_forget()
        button_get_xk.pack()
        buttona.pack()
        buttonb.pack()
        scroll_text.pack()
    else:
        try:
            buttona.pack_forget()
            buttonb.pack_forget()
        except:
            pass
        scroll_text.pack_forget()
        button_get_xk.pack_forget()
        label.pack()
        button_get_ps.pack()
        buttona.pack()
        buttonb.pack()


def on_else_change():
    if checkbutton_var.get():
        combobox2.pack(side=tk.BOTTOM, fill=tk.X)
        buttonc.pack()
    else:
        combobox2.pack_forget()
        buttonc.pack_forget()


def on_else_list_change(event):
    global elselist
    selected_mode = combobox2.get()
    XM.set(selected_mode)
    elselist = else_files[selected_mode]


tem = ["superhero", "vapor", "cyborg", "solar", "cosmo", "flatly", "journal", "litera", "minty", "pulse", "morph"]
root = ttk.Window(themename=tem[random.randint(0, 10)])
root.title("抽取学号")
root.attributes('-topmost', True)
root.iconbitmap('./ico.ico')
MS1 = tk.StringVar()
MS1.set("请选择模式")
XM = tk.StringVar()
XM.set("在此处选择抽取项目")
label = tk.Label(root, text="被抽中的学号是: ")
button_get_xk = ttk.Button(root, text="抽取学号", command=update_label, bootstyle="outline", width=30)
button_get_ps = ttk.Button(root, text="抽取学号", command=update_label1, bootstyle="outline", width=30)

buttona = ttk.Button(root, text="点击缩小窗口", command=create_float_window, bootstyle="outline", width=30)

buttonb = ttk.Button(root, text="修改学号范围", command=open_range_window, bootstyle="outline", width=30)

buttonc = ttk.Button(root, text="创建一个新的抽取项目", command=open_else_window, bootstyle="outline", width=30)
min_entry = tk.Entry(root)
max_entry = tk.Entry(root)

scroll_text = scrolledtext.ScrolledText(root, height=5, width=30)

load_range()
load_else()

credit_label = tk.Label(root, text="程序制作by：小於菟工作室、刘贞", font=("KaiTi", 12), anchor='se')
credit_label.pack(side=tk.BOTTOM, fill=tk.X)

mode_combobox1 = ttk.Combobox(root, values=["炫酷可视模式", "朴素快速模式"], textvariable=MS1)
mode_combobox1.pack(side=tk.BOTTOM, fill=tk.X)
mode_combobox1.bind("<<ComboboxSelected>>", on_mode_change)
checkbutton_var = tk.BooleanVar(value=False)
checkbutton = ttk.Checkbutton(root, text="启用避免单轮重复抽取", variable=checkbutton_var, command=on_else_change,
                              bootstyle="square-toggle")
checkbutton.pack()
combobox2 = ttk.Combobox(root, values=keys_list, textvariable=XM)
combobox2.bind("<<ComboboxSelected>>", on_else_list_change)
root.mainloop()
