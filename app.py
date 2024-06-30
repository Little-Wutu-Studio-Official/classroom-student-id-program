# 导入所需的库
import os
import pickle
import random
import sys
import threading
import time
import tkinter as tk
import tkinter.messagebox
from tkinter import scrolledtext

import numpy as np
import ttkbootstrap as ttk
from _tkinter import TclError

# 初始化变量x,y
x = None
y = None


# 判断已经抽取的学号列表中是否包含指定学号范围内的所有数字
def contains_all_numbers_between(lst, start, end):
    """
    判断已经抽取的学号列表中是否包含指定学号范围内的所有数字

    Args:
    lst: 待检查的列表
    start: 数字范围起始值
    end: 数字范围结束值

    Returns:
    如果列表中包含给定范围内的所有数字则返回True，否则返回False
    """
    expected_numbers = set(range(start, end + 1))  # 生成给定范围内的所有数字的集合
    list_set = set(lst)  # 将列表转换为集合
    return expected_numbers.issubset(list_set)  # 检查给定范围内的所有数字是否都包含在列表中


# 从指定范围内抽取学号
def draw_student_number(min_n, max_n):
    rng = np.random.default_rng()  # 创建随机数生成器
    # 如果避免单轮重复抽取复选框被选中（else.pickle文件中存在抽学号项目）
    if checkbutton_var.get():
        try:
            if_try = elselist
        except NameError:
            if_try = None
            tkinter.messagebox.showerror("错误", "在启用了避免单轮重复抽取功能的情况下，请先选择一个抽取项目再抽取学号！")
        while True:
            if if_try is not None:
                a = rng.integers(min_n, max_n + 1)
                # 如果抽取到的学号已经存在于elselist中并且elselist中不包含[min_n, max_n]范围内的所有数字（即学号已被抽到过且单轮并未抽完），就什么也不做,接着抽取一个。
                if a in elselist and not contains_all_numbers_between(elselist, min_n, max_n):
                    pass
                # 如果elselist中包含[min_n, max_n]范围内的所有数字，显示信息，进行重置
                elif contains_all_numbers_between(elselist, min_n, max_n):
                    elselist.clear()
                    tkinter.messagebox.showinfo("信息", f"项目{combobox2.get()}内所有学号都是幸运学号！该项目即将自动重置……")
                    else_files[combobox2.get()] = elselist
                    print(else_files)
                    save_else()
                # 第一次抽到：
                else:
                    elselist.append(a)
                    print(elselist)
                    else_files[combobox2.get()] = elselist
                    print(else_files)
                    save_else()
                    return a
            else:
                break
    else:
        # 如果复选框未被选中，则直接随机抽取学号
        return rng.integers(min_n, max_n + 1)


# 更新抽取框
def update_label():
    try:
        # 获取最小值输入框中的数值
        min_n = int(min_entry.get())
        # 获取最大值输入框中的数值
        max_n = int(max_entry.get())
    except TclError:
        os.execl(sys.executable, sys.executable, *sys.argv)
    # 清空滚动文本框
    scroll_text.delete(1.0, tk.END)

    # 创建线程并启动以绘制数字
    t = threading.Thread(target=draw_numbers, args=(min_n, max_n))
    t.start()


# 更新标签（朴素快速模式下的）
def update_label1():
    try:
        # 获取最小值输入框中的数值
        min_n = int(min_entry.get())
        # 获取最大值输入框中的数值
        max_n = int(max_entry.get())
    except TclError:
        os.execl(sys.executable, sys.executable, *sys.argv)
    # 调用draw_student_number函数获取随机学号
    drawn_number = draw_student_number(min_n, max_n)
    # 配置标签文本显示被抽中的学号
    label.config(text=f"被抽中的学号是: {drawn_number}")


# 保存范围设置
def save_range():
    # 检查是否抽取项目
    if else_files != {}:
        # 提示用户保存
        result = tk.messagebox.askyesno("保存？", "请注意，如果修改了学号范围，您的抽取项目将清空！")
        if result:
            # 如果用户选择保存，则删除抽学号项目文件并保存新的范围
            os.remove('./ranges/else.pickle')
    try:
        min_number = int(min_entry.get())
        max_number = int(max_entry.get())
        if min_number >= max_number:
            tkinter.messagebox.showerror("错误", "您输入的起始学号大于结束学号！请重新输入。")
        else:
            try:
                # 写入范围到文件
                with open('./ranges/range.txt', 'w') as f:
                    f.write(f"{min_number}\n{max_number}\n{initial_x}\n{initial_y}")
            except PermissionError:
                tkinter.messagebox.showerror("错误",
                                             "程序写入范围失败，可能是没有权限访问数据，请尝试以管理员身份运行程序或重新安装程序。")
            range_window.destroy()
            # 重新启动应用程序
            os.execl(sys.executable, sys.executable, *sys.argv)
    except ValueError:
        tkinter.messagebox.showerror("错误", "您输入的学号范围不是整数！请重新输入。")


# 修改项目名称
def change_program():
    # 获取选择框中的名称
    name = combobox_change_or_delete.get()
    # 如果名称为空，提示用户选择项目
    if name == "":
        tkinter.messagebox.showerror("错误", "请选择一个项目！")
    else:
        # 弹出修改项目名称窗口
        change_window = tk.Toplevel()
        change_window.grab_set()
        change_window.title("修改项目名称")
        label_change = tk.Label(change_window, text="请输入新的项目名称：")
        label_change.pack()
        # 创建输入框
        new_name = tk.StringVar()
        new_name_entry = tk.Entry(change_window, textvariable=new_name)
        new_name_entry.pack()
        # 创建确认按钮
        do = tk.Button(change_window, text="确认", command=lambda: change_name(new_name.get(), name))
        do.pack()

        def change_name(new_name_str, old_name_str):
            if new_name_str == "":
                tkinter.messagebox.showerror("错误", "请输入新的项目名称！")
            else:
                # 如果名称已存在，提示用户重新输入
                if new_name_str in else_files:
                    tkinter.messagebox.showerror("错误", "该名称已存在，请重新输入！")
                else:
                    # 修改项目名称
                    else_files[new_name_str] = else_files.pop(old_name_str)
                    # 保存修改后的项目名称
                    save_else()
                    # 关闭窗口
                    change_window.destroy()
                    # 重新加载抽取项目
                    load_else()
                    combobox2.config(values=keys_list)
                    # 重新启动抽取项目管理窗口
                    programs_window.destroy()
                    open_programs_window()
                    checkbutton_var.set(True)
                    on_else_change()
                    # 选择为刚刚修改的项目
                    combobox2.current(keys_list.index(new_name_str))
                    # 告知用户操作成功
                    tkinter.messagebox.showinfo("成功", "已成功修改项目名称！")


def delete_program():
    # 获取选择框中的名称
    name = combobox_change_or_delete.get()
    # 如果名称为空，提示用户选择项目
    if name == "":
        tkinter.messagebox.showerror("错误", "请选择一个项目！")
    else:
        # 弹出删除项目窗口
        delete_result = tkinter.messagebox.askyesno("删除项目", "确认删除该项目？")
        if delete_result:
            # 删除项目
            else_files.pop(name)
            save_else()
            tkinter.messagebox.showinfo("成功", "已成功删除该项目！")
            load_else()  # 重新加载抽取项目
            combobox2.config(values=keys_list)  # 更新下拉列表
            combobox2.set("在此处选择抽取项目")
            programs_window.destroy()


def review_lucky_people(program):
    if program == "":
        tkinter.messagebox.showerror("错误", "请选择一个项目！")
    else:
        # 弹出查看幸运学号窗口
        lucky_window = tk.Toplevel()
        lucky_window.grab_set()
        lucky_window.title(f"查看项目”{program}“中已经抽到的幸运学号")
        # 读取该项目中已经抽到的幸运学号
        lucky_list = else_files[program]
        lucky_window.iconbitmap('./ico.ico')  # 设置窗口图标

        def calculate_percentage(lst1, min_val1, max_val1):
            total_range = max_val1 - min_val1 + 1
            count_in_list = len([a for a in lst1 if min_val1 <= a <= max_val1])
            return round((count_in_list / total_range) * 100, 2)

        def create_groups(min_val1, max_val1):
            groups1 = []
            for a in range(min_val1, max_val1 + 1, 20):
                groups1.append((a, min(a + 19, max_val1)))
            return groups1

        def create_buttons(frame, lst1, start, end):
            for a in range(start, end + 1):
                btn = ttk.Button(frame, text=str(a), width=5)
                btn.grid(row=((a - start) // 5) % 4, column=(a - start) % 5, padx=5, pady=5)
                if a not in lst1:
                    btn.config(bootstyle="outline")

        def on_select(event):
            print(event)
            selected = combo.get()
            start, end = map(int, selected.split('-'))
            for widget in button_frame.winfo_children():
                widget.destroy()
            create_buttons(button_frame, lst, start, end)

        min_val = int(min_entry.get())
        max_val = int(max_entry.get())
        lst = lucky_list
        percentage = calculate_percentage(lst, min_val, max_val)
        Meter = ttk.Meter(lucky_window,
                          metersize=250,
                          amountused=percentage,
                          textright="%",
                          subtext=f'项目“{program}”,\n已产生{len(lst)}个幸运学号',
                          interactive=False,
                          meterthickness=20,
                          stripethickness=0)
        Meter.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW)
        groups = create_groups(min_val, max_val)
        combo_values = [f"{start}-{end}" for start, end in groups]
        combo = ttk.Combobox(lucky_window, values=combo_values)
        combo.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW)
        combo.bind("<<ComboboxSelected>>", on_select)
        combo.current(0)
        button_frame = ttk.Frame(lucky_window)
        button_frame.grid(row=2, column=0, columnspan=3, sticky=tk.NSEW)
        combo.event_generate("<<ComboboxSelected>>")
        ttk.Label(lucky_window, text="图例:").grid(row=3, column=0, sticky=tk.NSEW)
        ttk.Button(lucky_window, text="未抽到学号",  bootstyle="outline").grid(row=3, column=1, sticky=tk.NSEW)
        ttk.Button(lucky_window, text="已抽到学号").grid(row=3, column=2, sticky=tk.NSEW)


# 创建新的抽取项目
def new_else_list():
    name = name_else.get()
    if name in else_files:  # 检查名称是否已存在
        tkinter.messagebox.showerror("错误", "您输入了一个已经存在的名称，请重新输入")
    elif name == "":  # 检查名称是否为空
        tkinter.messagebox.showerror("错误", "请输入项目名称！")
    else:
        else_files[name] = []  # 添加新的项目
        with open('./ranges/else.pickle', 'wb') as f:  # 保存项目到文件
            pickle.dump(else_files, f)
        programs_window.destroy()  # 关闭窗口
        load_else()  # 重新加载抽取项目
        if len(keys_list) == 1:
            tkinter.messagebox.showinfo("首次创建？",
                                        "亲爱的用户\n在使用您创建的项目进行数次抽取后，\n您可以进入抽取项目管理系统查看统计数据哦！")
        checkbutton_var.set(True)
        on_else_change()
        XM.set("请选择一个抽取项目")
        combobox2.config(values=keys_list)  # 更新下拉列表
        # 选择为刚刚创建的项目
        combobox2.current(len(keys_list) - 1)
        # 激活选择项目事件
        combobox2.event_generate("<<ComboboxSelected>>")
        tkinter.messagebox.showinfo("注意",
                                    "抽取项目创建成功！\n\n但请您注意：\n每次启动程序时，如果您希望使用避免单轮重复抽取和统计功能\n请务必将避免重复抽取开关打开！")


# 保存抽取项目
def save_else():
    with open('./ranges/else.pickle', 'wb') as f:
        pickle.dump(else_files, f)


# 读取范围、窗口等设置
def load_range():
    # 加载学号范围信息
    # 使用global关键字修改全局变量initial_x, initial_y
    global initial_x, initial_y
    if os.path.exists('./ranges/range.txt'):
        try:
            with open('./ranges/range.txt', 'r') as f:
                # 读取学号范围文件中的最小值、最大值、以及窗口（缩小后的浮窗）的位置初始值
                min_number, max_number, initial_x, initial_y = f.read().splitlines()
                # 将最小值和最大值更新到对应的文本框中
                min_entry.delete(0, tk.END)
                min_entry.insert(0, min_number)
                max_entry.delete(0, tk.END)
                max_entry.insert(0, max_number)
            # 将初始值转换为整数
            initial_x = int(initial_x)
            initial_y = int(initial_y)
        except ValueError:
            with open('./ranges/range.txt', 'r') as f:
                # 读取学号范围文件中的最小值和最大值
                min_number, max_number = f.read().splitlines()
                # 将最大值更新到对应的文本框中
                max_entry.delete(0, tk.END)
                max_entry.insert(0, max_number)
            # 初始化学号范围的初始值为0
            initial_x = 0
            initial_y = 0
    else:
        # 如果学号范围文件不存在，弹出提示框询问用户是否设置学号范围
        result = tk.messagebox.askyesno("初始化学号范围", "系统检测到您没有初始化学号范围，请设置后再抽学号")
        if result:
            # 如果用户选择是，则打开设置学号范围窗口
            open_range_window()
        else:
            # 如果用户选择否，退出程序
            root.destroy()


# 读取抽取项目
# noinspection PyGlobalUndefined
def load_else():
    global else_files, keys_list
    else_files = {}  # 设置空字典
    if os.path.exists('./ranges/else.pickle'):  # 如果 else.pickle 文件存在
        with open('./ranges/else.pickle', 'rb') as f:  # 以只读方式打开 else.pickle 文件
            else_files = pickle.load(f)  # 加载文件内容到 else_files
    else:
        with open('./ranges/else.pickle', 'wb') as f:  # 以二进制写入方式打开 else.pickle 文件
            pickle.dump(else_files, f)  # 将空字典保存到文件中
    keys_list = list(else_files.keys())  # 获取 else_files 字典的键并转换为列表赋给 keys_list


# 打开修改学号范围的窗口
def open_range_window():
    global range_window  # 使用全局变量来存储范围窗口
    root.attributes('-topmost', False)  # 将根窗口设置为非置顶
    range_window = tk.Toplevel(root)  # 创建一个顶级窗口作为学号范围窗口
    range_window.title("修改学号范围")  # 设置窗口标题为"修改学号范围"
    range_window.grab_set()  # 给范围窗口设置抓取焦点
    range_window.iconbitmap('./ico.ico')  # 设置范围窗口的图标

    tk.Label(range_window, text="最小学号: ").pack()

    global min_entry  # 使用全局变量来存储最小学号的输入框
    min_entry = tk.Entry(range_window)  # 创建一个用于输入最小学号的输入框
    min_entry.pack()  # 将输入框放置到范围窗口中

    tk.Label(range_window, text="最大学号: ").pack()  # 创建标签，用于显示"最大学号"文本

    global max_entry  # 使用全局变量来存储最大学号的输入框
    max_entry = tk.Entry(range_window)  # 创建一个用于输入最大学号的输入框
    max_entry.pack()  # 将输入框放置到范围窗口中

    button = ttk.Button(range_window, text="保存范围", command=save_range)  # 创建一个按钮，用于保存学号范围，并绑定保存范围函数
    button.pack()  # 将按钮放置到范围窗口中


# 打开管理抽取项目的窗口
def open_programs_window():
    # 声明全局变量 programs_window
    global programs_window
    root.attributes('-topmost', False)  # 将根窗口置于最顶层
    programs_window = tk.Toplevel(root)  # 创建一个新的顶级窗口
    programs_window.title("抽取项目管理系统")  # 设置窗口标题
    programs_window.grab_set()  # 让此窗口获得焦点
    programs_window.iconbitmap('./ico.ico')  # 设置窗口图标
    for a in range(3):
        programs_window.rowconfigure(a, weight=1)
    Main_label = tk.Label(programs_window, text="抽取项目管理系统", font=("楷体", 30))
    Main_label.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW)

    change = ttk.Labelframe(programs_window, text="修改/删除项目：")
    change.grid(row=2, column=0, columnspan=1, sticky=tk.NSEW)
    for a in range(3):
        change.rowconfigure(a, weight=1)
    program_label = tk.Label(change, text="选择要修改或删除的项目：", font=("楷体", 20))
    program_label.grid(row=0, column=0, columnspan=2, sticky="NSEW")
    # 创建一个下拉列表，用于选择要修改或删除的项目
    global combobox_change_or_delete  # 声明全局变量 combobox_change_or_delete
    combobox_change_or_delete = ttk.Combobox(change, values=keys_list)
    combobox_change_or_delete.grid(row=1, columnspan=2, sticky="NSEW")
    # 创建按钮，用于修改或删除项目
    button_change_or_delete = ttk.Button(change, text="修改项目名", command=change_program)
    button_change_or_delete.grid(row=2, column=0, columnspan=1, sticky="NSEW")
    # 创建按钮，用于删除该项目
    button_delete = ttk.Button(change, text="删除项目", command=delete_program, style="NSEW")
    button_delete.grid(row=2, column=1, columnspan=1)

    new = ttk.Labelframe(programs_window, text="新建项目：")
    new.grid(row=1, column=0, columnspan=1, sticky=tk.NSEW)
    name_label = tk.Label(new, text="输入要创建的项目的名称：", font=("楷体", 20))
    name_label.grid(row=0, column=0, columnspan=1, sticky="NSEW")
    global name_else  # 声明全局变量 name_else
    name_else = tk.Entry(new)  # 创建输入框
    name_else.grid(row=1, columnspan=1, sticky="NSEW")  # 将输入框放置到窗口中
    button = ttk.Button(new, text="创建", command=new_else_list)  # 创建按钮并关联回调函数
    button.grid(row=2, columnspan=1, sticky="NSEW")  # 将按钮放置到窗口中

    review = ttk.Labelframe(programs_window, text="查看已抽到的幸运儿：")
    review.grid(row=3, column=0, columnspan=1, sticky=tk.NSEW)
    for a in range(3):
        review.rowconfigure(a, weight=1)
    lucky_label = tk.Label(review, text="选择要查看幸运儿的项目：", font=("楷体", 20))
    lucky_label.grid(row=0, column=0, columnspan=1, sticky="NSEW")
    # 创建一个下拉列表，用于选择要查看的项目
    global combobox_to_be_reviewed  # 声明全局变量 combobox_to_be_reviewed
    combobox_to_be_reviewed = ttk.Combobox(review, values=keys_list)
    combobox_to_be_reviewed.grid(row=1, columnspan=1, sticky="NSEW")
    # 创建按钮，用于查看已抽到的幸运儿
    button_review = ttk.Button(review, text="查看", command=lambda: review_lucky_people(combobox_to_be_reviewed.get()))
    button_review.grid(row=2, columnspan=1, sticky="NSEW")
    if not keys_list:
        programs_window.title("创建一个新的抽取项目")
        change.grid_forget()
        review.grid_forget()
        Label_welcome = ttk.Label(programs_window,
                                  text="初次进入项目管理系统？\n抽取项目的统计分析等功能\n还等待您的发现。\n请先创建一个抽取项目吧！",
                                  font=("楷体", 20))
        Label_welcome.grid(row=2, column=0, sticky=tk.NSEW)


initial_x = 0
initial_y = 0


# 创建浮动窗口
def create_float_window():
    global initial_x, initial_y
    # 创建一个浮动窗口
    float_window = tk.Toplevel(root)
    float_window.geometry(f"130x40+{initial_x}+{initial_y}")  # 设置浮动窗口的初始大小和位置
    float_window.overrideredirect(True)  # 隐藏浮动窗口的标题栏和边框
    float_window.attributes('-topmost', True)  # 将浮动窗口置顶显示

    button = ttk.Button(float_window, text="显示抽学号程序", command=lambda: show_main_window(float_window))
    button.pack(fill=tk.BOTH, expand=True)  # 将按钮放入浮动窗口并填充整个窗口
    # 使窗口可拖动
    float_window.bind("<ButtonPress-1>", lambda event: start_move(event))  # 绑定鼠标左键按下事件
    float_window.bind("<ButtonRelease-1>", lambda event: stop_move(float_window))  # 绑定鼠标左键释放事件
    float_window.bind("<B1-Motion>", lambda event: do_move(event, float_window))  # 绑定鼠标拖动事件
    root.withdraw()  # 隐藏主窗口


# 检查浮动窗口是否移动了
def has_moved(float_window):
    # 判断浮动窗口的当前位置是否和初始位置不同
    return float_window.winfo_x() != initial_x or float_window.winfo_y() != initial_y


# 显示主窗口
def show_main_window(float_window):
    # 如果按倒按钮但是浮动窗口没有移动，则执行以下操作
    if not has_moved(float_window):
        # 还原主窗口并销毁浮动窗口
        root.deiconify()
        float_window.destroy()


# 开始拖动窗口
def start_move(event):
    global x, y
    x = event.x
    y = event.y


# 停止拖动窗口
def stop_move(float_window):
    global x, y
    x = None
    y = None
    global initial_x, initial_y
    initial_x = float_window.winfo_x()
    initial_y = float_window.winfo_y()


# 拖动窗口
def do_move(event, float_window):
    deltax = event.x - x
    deltay = event.y - y
    x_ = float_window.winfo_x() + deltax
    y_ = float_window.winfo_y() + deltay
    float_window.geometry(f"+{x_}+{y_}")


def draw_numbers(min_number, max_number):
    # 调用函数获取学生学号
    b = draw_student_number(min_number, max_number)
    # 计算学号范围内的学号数量
    total_numbers = b - min_number + 1
    # 循环绘制学号
    for now_number in range(total_numbers):
        # 更新标签显示当前学号
        label.config(text=f"学号滚动区显示为{now_number + min_number}")
        # 在滚动文本框中插入当前学号信息
        scroll_text.insert(tk.END, f"当前学号是: {now_number + min_number}\n")
        # 滚动文本框滚动到末尾
        scroll_text.see(tk.END)
        # 更新界面
        root.update()
        # 计算当前学号展示的时间
        if now_number < total_numbers / 2:
            current_time = (7.5 / total_numbers) - ((now_number + 1) * (7.5 / total_numbers) / 2 / (total_numbers / 2))
        else:
            current_time = (7.5 / total_numbers) + (
                    (now_number - total_numbers / 2) * (7.5 / total_numbers) / 2 / (total_numbers / 2))
        if current_time > 0:
            time.sleep(current_time)


# 模式改变事件处理
# noinspection PyUnusedLocal
def on_mode_change(event):
    selected_mode = mode_combobox1.get()
    MS1.set(selected_mode)
    if selected_mode == "炫酷可视模式":
        try:
            buttona.grid_forget()
            buttonb.grid_forget()
        except TclError:
            pass
        label.grid(row=0, column=0, columnspan=1, sticky=tk.NSEW)
        button_get_ps.grid_forget()
        button_get_xk.grid(row=3, column=0, columnspan=1, sticky=tk.NSEW)
        buttona.grid(row=4, column=0, columnspan=1, sticky=tk.NSEW)
        buttonb.grid(row=5, column=0, columnspan=1, sticky=tk.NSEW)
        scroll_text.grid(row=6, column=0, columnspan=2, sticky=tk.NSEW)
    else:
        try:
            buttona.grid_forget()
            buttonb.grid_forget()
        except TclError:
            pass
        scroll_text.grid_forget()
        button_get_xk.grid_forget()
        label.grid(row=0, column=0, columnspan=1, sticky=tk.NSEW)
        button_get_ps.grid(row=3, column=0, columnspan=1, sticky=tk.NSEW)
        buttona.grid(row=4, column=0, columnspan=1, sticky=tk.NSEW)
        buttonb.grid(row=5, column=0, columnspan=1, sticky=tk.NSEW)
    save_model(selected_mode)


# 抽取项目选择状态变化事件处理
def on_else_change():
    if checkbutton_var.get():
        combobox2.grid(row=2, column=0, columnspan=1, sticky=tk.NSEW)
        load_else()
        if not keys_list:
            tkinter.messagebox.showwarning("警告", "系统检测到您目前没有抽取项目，\n请在抽取项目管理中新建一个。")
            open_programs_window()
    else:
        combobox2.grid_forget()


# 抽取项目列表变化事件处理
# noinspection PyUnusedLocal
def on_else_list_change(event):
    global elselist
    selected_mode = XM.get()
    if selected_mode == "在此处选择抽取项目":
        pass
    else:
        elselist = else_files[selected_mode]


def get_saved_window_position(window):
    try:
        with open('./ranges/window_position.pickle', 'rb') as file:
            x_place, y_place = pickle.load(file)
            window.geometry("+{}+{}".format(x_place, y_place))
    except FileNotFoundError:
        pass


def save_window_position(window):
    x_place, y_place = window.winfo_x(), window.winfo_y()
    with open('./ranges/window_position.pickle', 'wb') as file:
        pickle.dump((x_place, y_place), file)


def get_model():
    try:
        with open('./ranges/model.pickle', 'rb') as file:
            model = pickle.load(file)
            MS1.set(model)
            mode_combobox1.event_generate("<<ComboboxSelected>>")
    except FileNotFoundError:
        pass


def save_model(model):
    with open('./ranges/model.pickle', 'wb') as file:
        pickle.dump(model, file)


keys_list = []
tem = ["superhero", "vapor", "cyborg", "solar", "cosmo", "flatly", "journal", "litera", "minty", "pulse", "morph"]
root = ttk.Window(themename=tem[random.randint(0, 10)])
get_saved_window_position(root)
root.title("抽取学号")
root.attributes('-topmost', True)
root.iconbitmap('./ico.ico')
root.overrideredirect(False)
root.resizable(0, 0)
root.bind('<Configure>', lambda event: save_window_position(root))
MS1 = tk.StringVar()
MS1.set("请选择模式")
XM = tk.StringVar()
XM.set("在此处选择抽取项目")
for i in range(9):
    root.rowconfigure(i, weight=1)
label = tk.Label(root, text="被抽中的学号是: ", font=("KaiTi", 20))
button_get_xk = ttk.Button(root, text="抽取学号", command=update_label)
button_get_ps = ttk.Button(root, text="抽取学号", command=update_label1)

buttona = ttk.Button(root, text="点击缩小窗口", command=create_float_window)

buttonb = ttk.Button(root, text="修改学号范围", command=open_range_window)

min_entry = tk.Entry(root)
max_entry = tk.Entry(root)

scroll_text = scrolledtext.ScrolledText(root, height=3, width=10, font=("KaiTi", 20))

load_range()
load_else()

button_program = ttk.Button(root, text="抽取项目管理系统", command=open_programs_window)
button_program.grid(row=7, columnspan=1, sticky=tk.NSEW)
credit_label = tk.Label(root, text="制作：小於菟工作室（刘贞、王一格）", font=("KaiTi", 10))
credit_label.grid(row=9, column=0, columnspan=1, sticky=tk.NSEW)

mode_combobox1 = ttk.Combobox(root, values=["炫酷可视模式", "朴素快速模式"], textvariable=MS1)
mode_combobox1.grid(row=8, column=0, columnspan=1, sticky=tk.NSEW)
mode_combobox1.bind("<<ComboboxSelected>>", on_mode_change)
get_model()
checkbutton_var = tk.BooleanVar()
checkbutton = ttk.Checkbutton(root, text="启用避免单轮重复抽取", variable=checkbutton_var, command=on_else_change,
                              bootstyle="square-toggle")
checkbutton.grid(row=1, column=0, columnspan=1, sticky=tk.NSEW)
combobox2 = ttk.Combobox(root, values=keys_list, textvariable=XM)
combobox2.bind("<<ComboboxSelected>>", on_else_list_change)
root.mainloop()
