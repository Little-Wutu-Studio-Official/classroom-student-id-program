import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QMessageBox
from random import randint

class ClassroomLottery(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("课堂抽学号")
        self.setGeometry(100, 100, 300, 200)

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
        self.view_score_button.move(110, 120)
        self.view_score_button.clicked.connect(self.view_score)

    def lottery(self):
        student_numbers = [str(i).zfill(3) for i in range(1, 56)]
        lucky_number = str(randint(1, len(student_numbers))).zfill(3)
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
        dialog.setText(f"您抽到的学号是：{lucky_number}")
        dialog.exec()

    def view_score(self):
        score_text = ""
        for key, value in self.score.items():
            score_text += f"学号{key}：{value}分\n"
        dialog = QMessageBox()
        dialog.setWindowTitle("同学分数")
        dialog.setText(score_text)
        dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClassroomLottery()
    window.show()
    sys.exit(app.exec())


