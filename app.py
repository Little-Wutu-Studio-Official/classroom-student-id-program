# 导入所需的库
import math
import os
import pickle
import random
import threading
import time
import tkinter as tk
import tkinter.messagebox

import numpy as np
import ttkbootstrap as ttk

# 初始化变量x,y
x = None
y = None


def validate_number_bigger(text_input) -> bool:
    """验证输入数字比另一个大"""
    if text_input.isdigit() and min_entry.get().isdigit():
        if int(text_input) > int(min_entry.get()):
            return True
        else:
            return False
    elif text_input == "":
        return True
    else:
        return False


def validate_number(input_str) -> bool:
    """Validates that the input is a number"""
    if input_str.isdigit() and int(input_str) > 0:
        return True
    elif input_str == "":
        return True
    else:
        return False


# 判断已经抽取的学号列表中是否包含指定学号范围内的所有数字
def contains_all_numbers_between(lst, start, end) -> bool:
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
    # 如果避免单轮重复抽取复选框被选中（else.pickle文件中存在抽学号项目）
    if checkbutton_var.get():
        try:
            if_try = elselist
        except NameError:
            if_try = None
        while True:
            if if_try is not None:
                a = rng.integers(min_n, max_n + 1)
                # 如果抽取到的学号已经存在于elselist中并且elselist中不包含[min_n, max_n]范围内的所有数字（即学号已被抽到过且单轮并未抽完），就什么也不做,接着抽取一个。
                if a in elselist and not contains_all_numbers_between(elselist, min_n, max_n):
                    pass
                # 如果elselist中包含[min_n, max_n]范围内的所有数字，显示信息，进行重置
                elif contains_all_numbers_between(elselist, min_n, max_n):
                    elselist.clear()
                    tkinter.messagebox.showinfo("信息",
                                                f"项目{combobox2.get()}内所有学号都是幸运学号！该项目即将自动重置……")
                    else_files[combobox2.get()] = elselist
                    save_else()
                # 第一次抽到：
                else:
                    elselist.append(a)
                    else_files[combobox2.get()] = elselist
                    save_else()
                    return a
            else:
                tkinter.messagebox.showerror("错误",
                                             "在启用了避免单轮重复抽取功能的情况下，请先选择一个抽取项目再抽取学号！")
                return "No Choice Error"
    else:
        # 如果复选框未被选中，则直接随机抽取学号
        return rng.integers(min_n, max_n + 1)


# 更新抽取框
def update_label():
    show_number()
    # 创建线程并启动以绘制数字
    t = threading.Thread(target=draw_numbers, args=(min_number, max_number))
    t.start()


def show_number():
    global show_window
    show_window = tk.Toplevel()
    show_window.grab_set()
    show_window.overrideredirect(True)
    show_window.attributes('-topmost', True)

    global label1
    label = ttk.Label(show_window, text="幸运学号", font=("KaiTi", int(20 * txt_size)))
    label.grid(row=0, column=0, sticky=tk.NSEW)
    label1 = ttk.Label(show_window, text="", font=("KaiTi", int(140 * txt_size)))
    label1.grid(row=1, column=0, sticky=tk.NSEW)

    global Button_to_close
    Button_to_close = ttk.Button(show_window, text="关闭", command=show_window.destroy)
    Button_to_close.grid(column=0, row=2, sticky=tk.NSEW)

    global gauge
    gauge = ttk.Floodgauge(
        show_window,
        font=(None, int(20 * txt_size), 'bold'),
        mask="剩余时间:{}s",
        maximum=time_show,
        value=time_show,
    )

    if selected_mode == "炫酷可视模式":
        label.grid(row=1, column=0, sticky=tk.NSEW)
        gauge.grid(row=0, column=0, sticky=tk.NSEW)
        label1.grid(row=2, column=0, sticky=tk.NSEW)
        Button_to_close.grid(row=3, column=0, sticky=tk.NSEW)

    screen_width = show_window.winfo_screenwidth()
    screen_height = show_window.winfo_screenheight()
    show_window.update()
    window_width = show_window.winfo_width()
    window_height = show_window.winfo_height()
    x_place = (screen_width - window_width) // 2  # 居中计算 x坐标
    y_place = (screen_height - window_height) // 2  # 居中计算 y 坐标

    # 将窗口移到屏幕中心
    show_window.geometry("+{}+{}".format(x_place, y_place))


# 更新标签（朴素快速模式下的）
def update_label1():
    # 调用draw_student_number函数获取随机学号
    drawn_number = draw_student_number(min_number, max_number)
    if drawn_number == "No Choice Error":
        return
    # 显示抽取到的学号
    show_number()
    # 配置标签文本显示被抽中的学号
    if drawn_number < 10:
        label1.config(text=f"0{drawn_number}")
    else:
        label1.config(text=f"{drawn_number}")


# 保存范围设置
# noinspection PyUnboundLocalVariable
def save_range(min_num, max_num) -> bool:
    def do_save() -> bool:
        try:
            min_nu = min_num
            max_nu = max_num
            if min_nu >= max_nu:
                tkinter.messagebox.showerror("错误", "您输入的起始学号大于/等于结束学号！请尝试重新输入。")
                return False
            else:
                try:
                    # 写入范围到文件
                    with open('./ranges/range.txt', 'w') as f:
                        f.write(f"{min_nu}\n{max_nu}\n{initial_x}\n{initial_y}")
                    return True
                except PermissionError:
                    tkinter.messagebox.showerror("错误",
                                                 "程序写入范围失败，可能是没有权限访问数据，请尝试以管理员身份运行程序或重新安装程序。")
                    return False
        except ValueError:
            tkinter.messagebox.showerror("错误", "您输入的学号范围不是正整数！请重新输入。")
            return False
    try:
        if min_num == min_number and max_num == max_number:
            result_save = True
        else:
            # 检查是否抽取项目
            if else_files != {}:
                # 提示用户保存
                result = tk.messagebox.askyesno("保存？", "请注意，如果修改了学号范围，您的抽取项目将清空！")
                if result:
                    # 如果用户选择保存，则删除抽学号项目文件并保存新的范围
                    os.remove('./ranges/else.pickle')
                    result_save = do_save()
            else:
                result_save = do_save()
    except NameError:
        result_save = do_save()
    except ValueError:
        result_save = False
        # 提示用户输入数字范围以保存
        tkinter.messagebox.showwarning("警告",
                                       "请输入正整数学号范围以保存！\n请检查您的输入，\n并重新点击保存设置按钮以重试。")
    return result_save


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
        change_window.iconbitmap('./ico.ico')  # 设置窗口图标
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
            XM.set("在此处选择抽取项目")
            # 激活项目选择事件
            combobox2.event_generate("<<ComboboxSelected>>")
            # 关闭抽取项目管理窗口
            programs_window.destroy()


def review_lucky_people(program):
    if program == "":
        tkinter.messagebox.showerror("错误", "请选择一个项目！")
    else:
        # 弹出查看幸运学号窗口
        lucky_window = tk.Toplevel()
        lucky_window.grab_set()
        lucky_window.title(f"查看项目”{program}“中已经抽到的幸运学号")
        # 置顶查看幸运学号的窗口
        lucky_window.attributes('-topmost', True)
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

        # noinspection PyUnusedLocal
        def on_select(event):
            selected = combo.get()
            start, end = map(int, selected.split('-'))
            for widget in button_frame.winfo_children():
                widget.destroy()
            create_buttons(button_frame, lst, start, end)

        min_val = min_number
        max_val = max_number
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
        ttk.Button(lucky_window, text="未抽到学号", bootstyle="outline").grid(row=3, column=1, sticky=tk.NSEW)
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
        XM.set("在此处选择抽取项目")
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
    # 使用global关键字修改全局变量initial_x, initial_y, min_number, max_number
    global initial_x, initial_y, min_number, max_number
    if os.path.exists('./ranges/range.txt'):
        try:
            with open('./ranges/range.txt', 'r') as f:
                # 读取学号范围文件中的最小值、最大值、以及窗口（缩小后的浮窗）的位置初始值
                min_number, max_number, initial_x, initial_y = f.read().splitlines()
            # 将初始值转换为整数
            min_number = int(min_number)
            max_number = int(max_number)
            initial_x = int(initial_x)
            initial_y = int(initial_y)
        except ValueError:
            with open('./ranges/range.txt', 'r') as f:
                # 读取学号范围文件中的最小值和最大值
                min_number, max_number = f.read().splitlines()
            # 初始化学号范围的初始值为0
            initial_x = 0
            initial_y = 0
    else:
        # 如果学号范围文件不存在，弹出提示框询问用户是否设置学号范围
        result = tk.messagebox.askyesno("初始化学号范围", "系统检测到您没有初始化学号范围，请设置后再抽学号")
        if result:
            # 如果用户选择是，则打开设置学号范围窗口
            open_settings_window()
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


# 打开管理抽取项目的窗口
def open_programs_window():
    # 声明全局变量 programs_window
    global programs_window
    programs_window = tk.Toplevel(root)  # 创建一个新的顶级窗口
    programs_window.title("抽取项目管理系统")  # 设置窗口标题
    programs_window.grab_set()  # 让此窗口获得焦点
    programs_window.iconbitmap('./ico.ico')  # 设置窗口图标
    # 置顶programs_window
    programs_window.attributes('-topmost', True)
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


# 炫酷可视化模式下的更新标签逻辑函数
def draw_numbers(min_nu, max_nu):
    # 调用函数获取学生学号
    b = draw_student_number(min_nu, max_nu)
    if b == "No Choice Error":
        show_window.destroy()
        return
    # 计算学号范围内的学号数量
    total_numbers = b - min_nu + 1

    def generate_sequence_dict(number_of_data, sum_of_data):
        result = {}
        s = sum_of_data / number_of_data
        e = s / speed_show
        d = (s - e) / number_of_data
        for now in range(number_of_data):
            if now <= math.floor(number_of_data / 2):
                result[now] = s - d * now
            else:
                result[now] = s + d * (now - math.floor(number_of_data / 2))
        return result
    if total_numbers <= time_show / 2:
        # 直接将被抽取的幸运学号显示出来
        if b < 10:
            label1.config(text=f"0{b}")
        else:
            label1.config(text=str(b))
        gauge.configure(value=0)
        screen_width = show_window.winfo_screenwidth()
        screen_height = show_window.winfo_screenheight()
        show_window.update()
        window_width = show_window.winfo_width()
        window_height = show_window.winfo_height()
        x_place = (screen_width - window_width) // 2  # 居中计算 x坐标
        y_place = (screen_height - window_height) // 2  # 居中计算 y 坐标
        show_window.geometry("+{}+{}".format(x_place, y_place))  # 将窗口移到屏幕中心
        Button_to_close.config(state=tk.NORMAL)
        return
    elif total_numbers >= 75:
        start_number = total_numbers - random.randint(25, 75)
    else:
        start_number = min_nu
    global time_has_used
    time_list_first = generate_sequence_dict(total_numbers - start_number, time_show)
    time_has_used = 0
    Button_to_close.config(state=tk.DISABLED)
    for now_number in range(total_numbers - start_number):
        # 更新标签显示当前学号
        if now_number + start_number < 10:
            label1.config(text=f"0{now_number + start_number}")
        else:
            label1.config(text=f"{now_number + start_number}")
        time_has_used += time_list_first[now_number]
        time.sleep(time_list_first[now_number])
        gauge.configure(value=time_show - time_has_used)
        screen_width = show_window.winfo_screenwidth()
        screen_height = show_window.winfo_screenheight()
        show_window.update()
        window_width = show_window.winfo_width()
        window_height = show_window.winfo_height()
        x_place = (screen_width - window_width) // 2  # 居中计算 x坐标
        y_place = (screen_height - window_height) // 2  # 居中计算 y 坐标
        show_window.geometry("+{}+{}".format(x_place, y_place))  # 将窗口移到屏幕中心
    Button_to_close.config(state=tk.NORMAL)


# 模式改变事件处理
# noinspection PyUnusedLocal
def on_mode_change(event):
    global selected_mode
    selected_mode = mode_combobox1.get()
    MS1.set(selected_mode)
    if selected_mode == "炫酷可视模式":
        label_main.config(text="当前：炫酷可视模式")
        label_main.grid(row=0, column=0, columnspan=1, sticky=tk.NSEW)
        button_get_ps.grid_forget()
        button_get_xk.grid(row=3, column=0, columnspan=1, sticky=tk.NSEW)
        buttona.grid(row=4, column=0, columnspan=1, sticky=tk.NSEW)
    else:
        label_main.config(text="当前：朴素快速模式")
        button_get_xk.grid_forget()
        label_main.grid(row=0, column=0, columnspan=1, sticky=tk.NSEW)
        button_get_ps.grid(row=3, column=0, columnspan=1, sticky=tk.NSEW)
        buttona.grid(row=4, column=0, columnspan=1, sticky=tk.NSEW)
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
    mode_selected = XM.get()
    if mode_selected == "在此处选择抽取项目":
        elselist = None
    else:
        elselist = else_files[mode_selected]


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


def load_settings():
    global time_show, speed_show, txt_size
    try:
        with open('./ranges/settings.pickle', 'rb') as file:
            time_show, speed_show, txt_size = pickle.load(file)
    except FileNotFoundError:
        time_show = 8
        speed_show = 20
        txt_size = 1.0
        save_settings(False)


def save_settings(range_save):
    with open('./ranges/settings.pickle', 'wb') as file:
        pickle.dump((time_show, speed_show, txt_size), file)
    if range_save:
        try:
            min_num = int(min_entry.get())
            max_num = int(max_entry.get())
            result = save_range(min_num, max_num)
            tell = result
        except ValueError:
            result = False
            tell = result
    else:
        result, tell = False, True
    load_settings()
    load_else()
    if tell:
        tkinter.messagebox.showinfo("提示", "设置保存成功！")
    if result:
        load_range()
        settings_window.destroy()


def change_settings():
    global time_show, speed_show, txt_size
    time_show = round(scale_time.get(), 2)
    speed_show = round(scale_speed.get(), 2)
    txt_size = round(scale_txt.get(), 2)
    save_settings(True)


def back_default_settings():
    global time_show, speed_show, txt_size
    time_show = 8
    speed_show = 20
    txt_size = 1.0
    tkinter.messagebox.showinfo("提示", "已恢复默认设置！")
    save_settings(False)


def open_settings_window():
    def close():
        # 判断min_entry和max_entry是否为空，如果为空则弹出警告框，否则保存并关闭窗口
        if not min_entry.get() or not max_entry.get():
            tkinter.messagebox.showwarning("警告", "请您先设置学号范围。")
        else:
            settings_window.destroy()

    # noinspection PyUnusedLocal
    def change_txt_show(event):
        mun = round(scale_txt.get(), 2)
        try:
            label_show_scale_txt.config(text=f"当前滑杆示数：{mun}x")
        except NameError:
            pass

    # noinspection PyUnusedLocal
    def change_time_show(event):
        mun = round(scale_time.get(), 2)
        try:
            label_show_scale_time.config(text=f"当前滑杆示数：{mun}")
        except NameError:
            pass

    # noinspection PyUnusedLocal
    def change_speed_show(event):
        mun = round(scale_speed.get(), 2)
        try:
            label_show_scale_speed.config(text=f"当前滑杆示数：{mun}")
        except NameError:
            pass

    global settings_window
    settings_window = tk.Toplevel(root)
    settings_window.grab_set()
    settings_window.title("设置中心")
    settings_window.iconbitmap('./ico.ico')  # 设置窗口图标
    # 置顶设置窗口
    settings_window.attributes('-topmost', True)
    label_settings = tk.Label(settings_window, text="课堂抽学号小程序设置中心", font=("楷体", 20))
    label_settings.grid(row=0, columnspan=2, sticky=tk.NSEW)
    notebook = ttk.Notebook(settings_window)
    notebook.grid(row=1, columnspan=2, sticky=tk.NSEW)
    frame_range = ttk.Frame(settings_window)
    notebook.add(frame_range, text='学号范围设置')
    min_label = tk.Label(frame_range, text="最小学号: ", font=("楷体", 15))
    min_label.pack()
    number_func = settings_window.register(validate_number)  # 注册一个验证函数，用于检查输入是否为整数
    global min_entry  # 使用全局变量来存储最小学号的输入框
    min_entry = ttk.Entry(frame_range, validate="all", validatecommand=(number_func, '%P'))  # 创建一个用于输入最小学号的输入框
    min_entry.pack(fill=tk.X)  # 将输入框放置到范围窗口中
    tk.Label(frame_range, text="最大学号: ", font=("楷体", 15)).pack()  # 创建标签，用于显示"最大学号"文本
    global max_entry  # 使用全局变量来存储最大学号的输入框
    bigger_number_func = settings_window.register(validate_number_bigger)
    max_entry = ttk.Entry(frame_range, validate="focus", validatecommand=(bigger_number_func, '%P'))
    max_entry.pack(fill=tk.X)  # 将输入框放置到范围窗口中
    # 自动载入上一次保存的学号范围
    try:
        min_entry.insert(0, min_number)
        max_entry.insert(0, max_number)
    except NameError:
        pass

    frame_txt = ttk.Frame(settings_window)
    notebook.add(frame_txt, text='文本字体设置')
    ttk.Label(
        frame_txt,
        text="拉动滑块调整显示学号的字体大小：",
        font=("KaiTi", 15)
    ).grid(row=0, columnspan=3, sticky=tk.NSEW, padx=30)
    # 设置文本放大/缩小拉杆
    global scale_txt
    # 设置列的权重
    frame_txt.columnconfigure(0, weight=1)
    frame_txt.columnconfigure(1, weight=3)
    frame_txt.columnconfigure(2, weight=1)
    scale_txt = ttk.Scale(frame_txt, from_=0.50, to=3.00, command=change_txt_show)
    label_first = tk.Label(frame_txt, text="0.5x")
    label_last = tk.Label(frame_txt, text="3.0x")
    scale_txt.grid(row=2, column=1, columnspan=1, sticky=tk.NSEW)
    scale_txt.set(txt_size)
    label_first.grid(row=2, column=0, sticky=tk.NSEW)
    label_last.grid(row=2, column=2, sticky=tk.NSEW)
    label_show_scale_txt = tk.Label(frame_txt, text=f"当前滑杆示数：{round(txt_size, 2)}x", font=("KaiTi", 15))
    label_show_scale_txt.grid(row=3, columnspan=3, sticky=tk.NSEW)
    ttk.Label(
        frame_txt,
        text="此滑杆用于调整显示抽取学号的字体大小，\n不影响整个小程序的字体大小。",
        font=("KaiTi", 15)
    ).grid(row=4, columnspan=3, rowspan=2, sticky=tk.NSEW)

    frame_xkks = ttk.Frame(settings_window)
    notebook.add(frame_xkks, text='炫酷可视化模式设置')
    global time_show, speed_show
    time_label = tk.Label(frame_xkks, text="滚动特效显示时长：", font=("KaiTi", 15))
    time_label.grid(row=0, column=0, columnspan=3, sticky=tk.NSEW)
    ttk.Label(
        frame_xkks,
        text="拖动滑块调整特效显示时长：",
        font=("KaiTi", 15)
    ).grid(row=0, columnspan=3, sticky=tk.EW, padx=30)
    global scale_time
    # 设置列的权重
    frame_xkks.columnconfigure(0, weight=1)
    frame_xkks.columnconfigure(1, weight=5)
    frame_xkks.columnconfigure(2, weight=1)
    scale_time = ttk.Scale(frame_xkks, from_=2, to=30, command=change_time_show)
    label_first = tk.Label(frame_xkks, text="2s")
    label_last = tk.Label(frame_xkks, text="30s")
    scale_time.grid(row=2, column=1, columnspan=1, sticky=tk.NSEW)
    scale_time.set(time_show)
    label_first.grid(row=2, column=0, sticky=tk.NSEW)
    label_last.grid(row=2, column=2, sticky=tk.NSEW)
    label_show_scale_time = tk.Label(frame_xkks, text=f"当前滑杆示数：{round(time_show)}s")
    label_show_scale_time.grid(row=3, columnspan=3, sticky=tk.NSEW)
    ttk.Label(
        frame_xkks,
        text="滚动特效显示效果明显性：",
        font=("KaiTi", 15)
    ).grid(row=5, columnspan=3, sticky=tk.EW, padx=30)
    global scale_speed
    scale_speed = ttk.Scale(frame_xkks, from_=10, to=30, command=change_speed_show)
    label_first = tk.Label(frame_xkks, text="10")
    label_last = tk.Label(frame_xkks, text="30")
    scale_speed.grid(row=7, column=1, columnspan=1, sticky=tk.NSEW)
    scale_speed.set(speed_show)
    label_first.grid(row=7, column=0, sticky=tk.NSEW)
    label_last.grid(row=7, column=2, sticky=tk.NSEW)
    label_show_scale_speed = tk.Label(frame_xkks, text=f"当前滑杆示数：{round(speed_show)}")
    label_show_scale_speed.grid(row=8, columnspan=3, sticky=tk.NSEW)

    Button_to_back = ttk.Button(settings_window, text="恢复默认设置(不更改学号范围)", bootstyle="outline",
                                command=back_default_settings)
    Button_to_back.grid(row=2, column=1, columnspan=1, sticky=tk.NSEW)
    Button_to_close_window = ttk.Button(settings_window, text="关闭设置中心", bootstyle="outline",
                                        command=close)
    Button_to_close_window.grid(row=3, columnspan=2, sticky=tk.NSEW)
    Button_to_save = ttk.Button(settings_window, text="保存全部以上设置", bootstyle="outline", command=change_settings)
    Button_to_save.grid(row=2, column=0, columnspan=1, sticky=tk.NSEW)


rng = np.random.default_rng()  # 创建随机数生成器
keys_list = []
load_settings()
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
label_main = tk.Label(root, text="当前：", font=("KaiTi", 20))
button_get_xk = ttk.Button(root, text="抽取学号", command=update_label, bootstyle="outline")
button_get_ps = ttk.Button(root, text="抽取学号", command=update_label1, bootstyle="outline")

buttona = ttk.Button(root, text="点击缩小窗口", command=create_float_window, bootstyle="outline")

min_entry = tk.Entry(root)
max_entry = tk.Entry(root)

load_range()
load_else()

button_program = ttk.Button(root, text="抽取项目管理系统", command=open_programs_window, bootstyle="outline")
button_program.grid(row=5, columnspan=1, sticky=tk.NSEW)

button_settings = ttk.Button(root, text="课堂抽学号小程序设置", command=open_settings_window, bootstyle="outline")
button_settings.grid(row=6, columnspan=1, sticky=tk.NSEW)
credit_label = tk.Label(root, text="制作：小於菟工作室（刘贞、王一格）", font=("KaiTi", 10))
credit_label.grid(row=8, column=0, columnspan=1, sticky=tk.NSEW)

mode_combobox1 = ttk.Combobox(root, values=["炫酷可视模式", "朴素快速模式"], textvariable=MS1)
mode_combobox1.grid(row=7, column=0, columnspan=1, sticky=tk.NSEW)
mode_combobox1.bind("<<ComboboxSelected>>", on_mode_change)
get_model()
checkbutton_var = tk.BooleanVar()
checkbutton = ttk.Checkbutton(root, text="启用避免单轮重复抽取", variable=checkbutton_var, command=on_else_change,
                              bootstyle="square-toggle")
checkbutton.grid(row=1, column=0, columnspan=1, sticky=tk.NSEW)
combobox2 = ttk.Combobox(root, values=keys_list, textvariable=XM)
combobox2.bind("<<ComboboxSelected>>", on_else_list_change)
root.mainloop()
