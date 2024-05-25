# 导入所需的库
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
def draw_student_number(min_number, max_number):
    # 如果避免单轮重复抽取复选框被选中（else.pickle文件中存在抽学号项目）
    if checkbutton_var.get():
        while True:
            a = random.randint(min_number, max_number)
            # 如果抽取到的学号已经存在于elselist中并且elselist中不包含[min_number, max_number]范围内的所有数字（即学号已被抽到过且单轮并未抽完），就什么也不做,接着抽取一个。
            if a in elselist and not contains_all_numbers_between(elselist, min_number, max_number):
                pass
            # 如果elselist中包含[min_number, max_number]范围内的所有数字，显示信息，进行重置
            elif contains_all_numbers_between(elselist, min_number, max_number):
                elselist.clear()
                tkinter.messagebox.showinfo("信息", "该抽取项目内所有人都已经被抽取过了，即将自动重置……")
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
        # 如果复选框未被选中，则直接随机抽取学号
        return random.randint(min_number, max_number)


# 更新抽取框
def update_label():
    # 获取最小值输入框中的数值
    min_number = int(min_entry.get())
    # 获取最大值输入框中的数值
    max_number = int(max_entry.get())

    # 清空滚动文本框
    scroll_text.delete(1.0, tk.END)

    # 创建线程并启动以绘制数字
    t = threading.Thread(target=draw_numbers, args=(min_number, max_number))
    t.start()


# 更新标签（朴素快速模式下的）
def update_label1():
    # 获取最小值输入框中的数值
    min_number = int(min_entry.get())
    # 获取最大值输入框中的数值
    max_number = int(max_entry.get())
    # 调用draw_student_number函数获取随机学号
    drawn_number = draw_student_number(min_number, max_number)
    # 配置标签文本显示被抽中的学号
    label.config(text=f"被抽中的学号是: {drawn_number}")


# 保存范围设置
def save_range():
    global max_number, min_number
    w = False
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
            tkinter.messagebox.showerror("错误", "您输入的最小学号大于或等于最大学号！请重新输入。")
            w = True
    except:
        tkinter.messagebox.showerror("错误", "您输入的学号范围不是整数！请重新输入。")
        w = True
    if not w:
        try:
            # 写入范围到文件
            with open('./ranges/range.txt', 'w') as f:
                f.write(f"{min_number}\n{max_number}\n{initial_x}\n{initial_y}")
            range_window.destroy()
            # 重新启动应用程序
            os.execl(sys.executable, sys.executable, *sys.argv)
        except:
            tkinter.messagebox.showerror("错误", "程序写入范围失败，请重新安装并不要改变预置路径！")
    else:
        pass


# 创建新的抽取项目
def new_else_list():
    name = name_else.get()
    if name in else_files:  # 检查名称是否已存在
        tkinter.messagebox.showerror("错误", "您输入了一个已经存在的名称，请重新输入")
    else:
        else_files[name] = []  # 添加新的项目
        with open('./ranges/else.pickle', 'wb') as f:  # 保存项目到文件
            pickle.dump(else_files, f)
        programs_window.destroy()  # 关闭窗口
        tk.messagebox.askyesno("增加新的项目", "为了使得更改生效，请手动重启程序。")  # 提示用户重启程序使更改生效


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
        except:
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
            os.execl(sys.executable, *sys.argv)


# 读取抽取项目
def load_else():
    global else_files, keys_list
    if os.path.exists('./ranges/else.pickle'):  # 如果 else.pickle 文件存在
        with open('./ranges/else.pickle', 'rb') as f:  # 以只读方式打开 else.pickle 文件
            else_files = pickle.load(f)  # 加载文件内容到 else_files
    else:
        else_files = {}  # 设置空字典
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

    label = tk.Label(range_window, text="最小学号: ")  # 创建标签，用于显示"最小学号"文本
    label.pack()  # 将标签放置到范围窗口中

    global min_entry  # 使用全局变量来存储最小学号的输入框
    min_entry = tk.Entry(range_window)  # 创建一个用于输入最小学号的输入框
    min_entry.pack()  # 将输入框放置到范围窗口中

    label = tk.Label(range_window, text="最大学号: ")  # 创建标签，用于显示"最大学号"文本
    label.pack()  # 将标签放置到范围窗口中

    global max_entry  # 使用全局变量来存储最大学号的输入框
    max_entry = tk.Entry(range_window)  # 创建一个用于输入最大学号的输入框
    max_entry.pack()  # 将输入框放置到范围窗口中

    button = ttk.Button(range_window, text="保存范围", command=save_range)  # 创建一个按钮，用于保存学号范围，并绑定保存范围函数
    button.pack()  # 将按钮放置到范围窗口中


# 打开创建新的抽取项目的窗口
def open_else_window():
    # 声明全局变量 programs_window
    global programs_window
    root.attributes('-topmost', False)  # 将根窗口置于最顶层
    programs_window = tk.Toplevel(root)  # 创建一个新的顶级窗口
    programs_window.title("创建一个新的抽取项目")  # 设置窗口标题
    programs_window.grab_set()  # 让此窗口获得焦点
    programs_window.iconbitmap('./ico.ico')  # 设置窗口图标

    label = tk.Label(programs_window, text="请输入名称")  # 创建标签
    label.pack()  # 将标签放置到窗口中

    global name_else  # 声明全局变量 name_else
    name_else = tk.Entry(programs_window)  # 创建输入框
    name_else.pack()  # 将输入框放置到窗口中

    button = ttk.Button(programs_window, text="创建", command=new_else_list)  # 创建按钮并关联回调函数
    button.pack()  # 将按钮放置到窗口中


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
    float_window.bind("<ButtonPress-1>", lambda event: start_move(event, float_window))  # 绑定鼠标左键按下事件
    float_window.bind("<ButtonRelease-1>", lambda event: stop_move(event, float_window))  # 绑定鼠标左键释放事件
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
def start_move(event, float_window):
    global x, y
    x = event.x
    y = event.y


# 停止拖动窗口
def stop_move(event, float_window):
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
    for i in range(total_numbers):
        # 更新标签显示当前学号
        label.config(text=f"学号滚动区显示为{i + min_number}")
        # 在滚动文本框中插入当前学号信息
        scroll_text.insert(tk.END, f"当前学号是: {i + min_number}\n")
        # 滚动文本框滚动到末尾
        scroll_text.see(tk.END)
        # 更新界面
        root.update()
        # 计算当前学号展示的时间
        if i < total_numbers / 2:
            current_time = (7.5 / total_numbers) - ((i + 1) * (7.5 / total_numbers) / 2 / (total_numbers / 2))
        else:
            current_time = (7.5 / total_numbers) + (
                    (i - total_numbers / 2) * (7.5 / total_numbers) / 2 / (total_numbers / 2))
        if current_time > 0:
            time.sleep(current_time)


# 模式改变事件处理
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
    save_model(selected_mode)


# 抽取项目选择状态变化事件处理
def on_else_change():
    if checkbutton_var.get():
        combobox2.pack(side=tk.BOTTOM, fill=tk.X)
        buttonc.pack()
    else:
        combobox2.pack_forget()
        buttonc.pack_forget()


# 抽取项目列表变化事件处理
def on_else_list_change(event):
    global elselist
    selected_mode = combobox2.get()
    XM.set(selected_mode)
    elselist = else_files[selected_mode]


def get_saved_window_position(window):
    try:
        with open('./ranges/window_position.pickle', 'rb') as file:
            x, y = pickle.load(file)
            window.geometry("+{}+{}".format(x, y))
    except (FileNotFoundError, ValueError):
        pass


def save_window_position(window, event):
    x, y = window.winfo_x(), window.winfo_y()
    with open('./ranges/window_position.pickle', 'wb') as file:
        pickle.dump((x, y), file)


def get_model(root):
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


tem = ["superhero", "vapor", "cyborg", "solar", "cosmo", "flatly", "journal", "litera", "minty", "pulse", "morph"]
root = ttk.Window(themename=tem[random.randint(0, 10)])
root.title("抽取学号")
root.attributes('-topmost', True)
root.iconbitmap('./ico.ico')
root.bind('<Configure>', lambda event: save_window_position(root, event))
root.bind('<Map>', lambda event: get_saved_window_position(root))
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

credit_label = tk.Label(root, text="制作：小於菟工作室（刘贞、王一格）", font=("KaiTi", 10), anchor='se')
credit_label.pack(side=tk.BOTTOM, fill=tk.X)

mode_combobox1 = ttk.Combobox(root, values=["炫酷可视模式", "朴素快速模式"], textvariable=MS1)
mode_combobox1.pack(side=tk.BOTTOM, fill=tk.X)
mode_combobox1.bind("<<ComboboxSelected>>", on_mode_change)
get_model(root)
checkbutton_var = tk.BooleanVar(value=False)
checkbutton = ttk.Checkbutton(root, text="启用避免单轮重复抽取", variable=checkbutton_var, command=on_else_change,
                              bootstyle="square-toggle")
checkbutton.pack()
combobox2 = ttk.Combobox(root, values=keys_list, textvariable=XM)
combobox2.bind("<<ComboboxSelected>>", on_else_list_change)
root.mainloop()
