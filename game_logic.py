import os
import random

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def get_max_score():
    if os.path.isfile("win.txt"):
        with open("win.txt", "r") as result_file:
            return int(result_file.read(), 2)
    else:
        return 0


def set_max_score(max_score):
    with open("win.txt", "w") as result_file:
        result_file.write(bin(max_score))


class Game(QMainWindow):

    def __init__(self, resolution, theme, parent=None):
        super().__init__(parent)
        self.colors = ['#34486a', '',
                       '#cad877', '#d7ddea', '#fec77f', '#ffb3b1',
                       '#c0eb7e', '#c2e4eb', '#ffea97', '#f9c0c9',
                       '#778046', '#757980', '#c78b89']
        self.setWindowTitle("2048")
        self.resolution = resolution
        self.theme = theme
        self.size = 4
        self.x = self.size * (resolution[0] / 25)
        self.board = self.createBoard
        self.score = [0, 0]
        self.moved = False
        self.setWindowIcon(QIcon('images/logo.png'))
        self.setStyleSheet("background-color: " + self.theme + ";")
        self.setFixedSize(self.resolution[0], self.resolution[1])
        self.setWindowTitle("2048")
        self.show()
        self.score[0] = get_max_score()

    @property
    def createBoard(self):
        return [[0 for _ in range(self.size)] for _ in range(self.size)]

    def set_board(self, x, y, value):
        if 0 <= x < self.size and 0 <= y < self.size:
            self.board[x][y] = value

    def get_board(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.board[x][y]
        return -1

    def turn(self, old_x, old_y, direction_x, direction_y):
        if self.get_board(old_x, old_y) > 0:
            while self.get_board(old_x + direction_x, old_y + direction_y) == 0:
                self.board[old_x + direction_x][old_y + direction_y] = self.get_board(old_x, old_y)
                self.board[old_x][old_y] = 0
                old_x += direction_x
                old_y += direction_y
                self.moved = True

    def joint(self, old_x, old_y, direction_x, direction_y):
        if self.get_board(old_x, old_y) > 0:
            if self.get_board(old_x + direction_x, old_y + direction_y) == self.get_board(old_x, old_y):
                self.set_board(old_x + direction_x, old_y + direction_y, self.get_board(old_x, old_y) * 2)
                self.score[1] += self.get_board(old_x, old_y) * 2
                while self.get_board(old_x - direction_x, old_y - direction_y) > 0:
                    self.set_board(old_x, old_y, self.get_board(old_x - direction_x, old_y - direction_y))
                    old_x -= direction_x
                    old_y -= direction_y
                self.set_board(old_x, old_y, 0)
                self.moved = True

    def lose_check(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.get_board(x, y) == 0:
                    return False
        for x in range(self.size):
            for y in range(self.size):
                if self.get_board(x, y) == self.get_board(x + 1, y) \
                        or self.get_board(x, y) == self.get_board(x, y + 1):
                    return False
        return True

    def win_check(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.get_board(x, y) == 2048:
                    return True

    def click(self, event):
        if event == 0:
            self.moved = False
            for j in range(self.size):
                for i in range(self.size):
                    self.turn(i, j, -1, 0)
                for i in range(self.size):
                    self.joint(i, j, -1, 0)
            if self.moved:
                self.generate(self.board, self.size)

        elif event == 1:
            self.moved = False
            for i in range(self.size):
                for j in range(self.size):
                    self.turn(i, j, 0, -1)
                for j in range(self.size):
                    self.joint(i, j, 0, -1)
            if self.moved:
                self.generate(self.board, self.size)

        elif event == 2:
            self.moved = False
            for j in range(self.size):
                for i in range(2, -1, -1):
                    self.turn(i, j, 1, 0)
                for i in range(2, -1, -1):
                    self.joint(i, j, 1, 0)
            if self.moved:
                self.generate(self.board, self.size)

        elif event == 3:
            self.moved = False
            for i in range(self.size):
                for j in range(2, -1, -1):
                    self.turn(i, j, 0, 1)
                for j in range(2, -1, -1):
                    self.joint(i, j, 0, 1)
            if self.moved:
                self.generate(self.board, self.size)

        elif event == 4:
            if self.lose_check() == 1:
                for i in range(self.size):
                    for j in range(self.size):
                        self.set_board(i, j, 0)
                self.score[1] = 0
            if sum([sum([i for i in j]) for j in self.board]) == 0:
                self.generate(self.board, self.size)
        elif event == 5:
           self.close()

        self.update()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Left:
            self.click(0)
        elif e.key() == Qt.Key_Right:
            self.click(2)
        elif e.key() == Qt.Key_Down:
            self.click(3)
        elif e.key() == Qt.Key_Up:
            self.click(1)
        elif e.key() == Qt.Key_Enter:
            self.click(4)
        elif e.key()== Qt.Key_D:
            self.click(5)

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)
        qp.begin(self)
        if self.theme == "gray":
            tcolor = "#000000"
        elif self.theme == "white":
            tcolor = "#ffffff"
        pen = QPen(QColor(tcolor))
        qp.drawRect(self.x, self.x, self.x * 4, self.x * 4)
        qp.setPen(pen)
        for ex in range(self.size):
            for ey in range(self.size):
                qp.setFont(QFont('Calibri', 30))
                c1 = ex * self.x + self.x
                c2 = ey * self.x + self.x
                if not self.lose_check():
                    k = len(str(bin(self.board[ex][ey]))) - 2
                    if k == 1:
                        qp.fillRect(c1, c2, self.x, self.x, QBrush(QColor(tcolor)))
                    else:
                        qp.fillRect(c1, c2, self.x, self.x, QBrush(QColor(self.colors[k])))
                qp.drawText(c1, c2, self.x, self.x, Qt.AlignHCenter | Qt.AlignVCenter, str(self.board[ex][ey]))

        pen = QPen(QColor(self.colors[0]))
        qp.setPen(pen)
        qp.setFont(QFont('Calibri', 20))
        qp.drawText(-10 + self.resolution[0] * 2 / 5, self.resolution[0] * 4 / 5, 130, 53, Qt.AlignHCenter,
                    "Score: " + str(self.score[1]))
        if self.lose_check():
            qp.drawText(175, 300, 120, 53, Qt.AlignHCenter, "Game Over")
            self.save_new_score()
        elif self.win_check():
            qp.drawText(self.resolution[0] * 2 / 5, 30 + self.resolution[0] * 4 / 5, 120, 53, Qt.AlignHCenter,
                        "You won!")
            self.save_new_score()

        pen = QPen(QColor('#b0b5b5'))
        qp.setPen(pen)
        qp.setFont(QFont('Calibri', 14))
        qp.drawText(self.resolution[0] * 2 / 5, 35 + self.resolution[0] * 4 / 5, 116, 53, Qt.AlignHCenter,
                    "Record: " + str(self.score[0]))
        pen = QPen(QColor('#000000'))
        qp.setFont(QFont('Century Gothic', 16))
        qp.setPen(pen)
        qp.drawText(self.resolution[0] * 2 / 5,  self.resolution[0] / 12, 116, 53, Qt.AlignHCenter,
                    "Exit")
        qp.drawRect(self.resolution[0] * 2 / 5+7,  self.resolution[0] / 12, 100, 25)
        qp.end()


    @staticmethod
    def generate(field, size):
        while True:
            random_x = random.randrange(0, size)
            random_y = random.randrange(0, size)
            if field[random_x][random_y] == 0:
                field[random_x][random_y] = random.choice([2] * 9 + [4] * 1)
                break

    def save_new_score(self):
        if self.score[1] > self.score[0]:
            set_max_score(self.score[1])
            self.score[0] = self.score[1]
        else:
            set_max_score(self.score[0])

    def on_click_s(self):
        self.close()
