import sys
import os
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QMessageBox, QDesktopWidget, QWidget

class ClassroomLottery(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("课堂抽学号")
        self.setFixedSize(300, 200)
        self.move(QDesktopWidget().availableGeometry().center() - self.frameGeometry().center())

        self.teacher_mode = True

        self.label = QLabel(self)
        self.label.setText("点击按钮抽取学号")
        self.label.move(80, 40)

        self.button = QPushButton("抽取", self)
        self.button.move(110, 70)
        self.button.clicked.connect(self.lottery)

        self.score_count = {f"{i:03}" for i in range(1, 56)}
        self.score = {key: 0 for key in self.score_count}

        self.view_score_button = QPushButton("查看分数", self)
        self.view_score_button.move(30, 160)
        self.view_score_button.clicked.connect(self.view_score)

        self.group_button = QPushButton("设置分组", self)
        self.group_button.move(170, 160)
        self.group_button.clicked.connect(self.set_group)

        self.group = {}
        self.load_group()

    def load_group(self):
        if os.path.exists('group.json'):
            with open('group.json', 'r') as f:
                self.group = json.load(f)

    def save_group(self):
        with open('group.json', 'w') as f:
            json.dump(self.group, f)

    def lottery(self):
        student_numbers = [str(i).zfill(3) for i in range(1, 56)]
        lucky_number = str(student_numbers[0])
        if lucky_number not in self.group:
            self.group[lucky_number] = "未分组"
        dialog = QMessageBox()
        dialog.setWindowTitle("是否获得加分？")
        dialog.setText(f"学号{lucky_number}是否获得1分？")
        dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = dialog.exec()
        if result == QMessageBox.Yes:
            self.score[lucky_number] += 1
        else:
            dialog = QMessageBox()
            dialog.setWindowTitle("是否扣分？")
            dialog.setText(f"学号{lucky_number}是否扣1分？")
            dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            result = dialog.exec()
            if result == QMessageBox.Yes:
                self.score[lucky_number] -= 1
        self.label.setText(f"恭喜你，获得学号 {lucky_number}")
        dialog = QMessageBox()
        dialog.setWindowTitle("抽到的学号")
        dialog.setText(f"您抽到的学号是：{lucky_number}，分组为：{self.group[lucky_number]}")
        dialog.exec()

    def view_score(self):
        score_text = ""
        for key, value in self.score.items():
            score_text += f"学号{key}：{value}分\n"
        dialog = QMessageBox()
        dialog.setWindowTitle("同学分数")
        dialog.setText(score_text)
        dialog.exec()

    def set_group(self):
        dialog = QMessageBox()
        dialog.setWindowTitle("设置分组")
        dialog.setText("请输入学号和分组名，以逗号隔开：")
        dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        result = dialog.exec()
        if result == QMessageBox.Ok:
            text = dialog.textValue().strip()
            if "," not in text:
                QMessageBox.warning(self, "错误", "输入格式错误，请输入学号和分组名，以逗号隔开。")
                return
            key, value = text.split(",")
            key = key.strip()
            value = value.strip()
            if key not in self.score:
                QMessageBox.warning(self, "错误", "输入学号不存在，请重新输入。")
                return
            self.group[key] = value
            self.save_group()
            QMessageBox.information(self, "设置成功", f"学号{key}的分组已设为{value}。")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClassroomLottery()



