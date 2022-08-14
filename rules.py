import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from ui.sourcecode.RulesWindow import Ui_Form


class Rules(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon('images/logo.png'))
        self.ui.button.clicked.connect(self.onClicked)

    def onClicked(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = Rules()
    screen.show()
    sys.exit(app.exec_())
