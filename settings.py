import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QButtonGroup

from ui.sourcecode.SettingsWindow import Ui_Form
from game_logic import Game


class Settings(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("Settings")
        self.resolution = [450, 600]
        self.theme = "white"
        self.buttongroup = QButtonGroup()
        self.buttongroup2 = QButtonGroup()
        self.setWindowIcon(QIcon('images/logo.png'))
        self.ui.radioButton4.resolution = [500, 500]
        self.buttongroup.addButton(self.ui.radioButton4)
        self.ui.radioButton4.toggled.connect(self.onClicked)

        self.ui.radioButton3.resolution = [450, 600]
        self.buttongroup.addButton(self.ui.radioButton3)
        self.ui.radioButton3.toggled.connect(self.onClicked)

        self.ui.radioButton5.resolution = [800, 800]
        self.buttongroup.addButton(self.ui.radioButton5)
        self.ui.radioButton5.toggled.connect(self.onClicked)

        self.ui.radioButton2.theme = "white"
        self.ui.radioButton2.toggled.connect(self.onClickedTheme)
        self.buttongroup2.addButton(self.ui.radioButton2)

        self.ui.radioButton.theme = "gray"
        self.ui.radioButton.toggled.connect(self.onClickedTheme)
        self.buttongroup2.addButton(self.ui.radioButton)

        self.ui.game_button.clicked.connect(self.on_click)

    def onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.resolution = radioButton.resolution

    @pyqtSlot()
    def on_click(self):
        self.win = Game(self.resolution, self.theme)
        self.win.show()

    def onClickedTheme(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            if radioBtn.theme is not None:
                self.theme = radioBtn.theme


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Settings()
    win.show()
    sys.exit(app.exec_())
