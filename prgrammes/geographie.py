import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, 
        QMenuBar, QMenu)


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.menuBar = QMenuBar()
        fileMenu = self.menuBar.addMenu('Fichier')

        nouveauMenu = QMenu('Nouveau', self)

        fileMenu.addMenu(nouveauMenu)

        self.setGeometry(330, 100, 800, 600)
        self.setWindowTitle('Géographe')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
