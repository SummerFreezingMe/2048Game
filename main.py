import sys

from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QMainWindow

from game_logic import Game
from rules import Rules
from settings import Settings
from ui.sourcecode.MainWindow import Ui_MainWindow


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('images/logo.png'))
        self.ui.game_button.clicked.connect(self.on_click)
        self.ui.settings_button.clicked.connect(self.on_click_s)
        self.ui.rules_button.clicked.connect(self.on_click_r)
        self.ui.author.clicked.connect(self.on_click_a)

    @pyqtSlot()
    def on_click(self):
        self.w2 = Game([500, 500], "white")
        self.w2.show()
        self.hide()

    def on_click_s(self):
        self.w2 = Settings()
        self.w2.show()

    def on_click_r(self):
        self.w2 = Rules()
        self.w2.show()

    def on_click_a(self):
        QDesktopServices.openUrl(QUrl("https://vk.com/ledesordrecestmoi"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
