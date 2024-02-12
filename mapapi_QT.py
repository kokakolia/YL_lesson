import sys
from io import BytesIO

import requests
from PIL import Image, ImageQt
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QAction
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QToolBar, QMainWindow, QMenu

SCREEN_SIZE = [600, 450]


class Example(QMainWindow):
    def __init__(self, map_api_server, map_params):
        super().__init__()
        self.map_api_server = map_api_server
        self.map_params = map_params
        self.scroll_value = 0.01
        self.initUI()

    def getImage(self):
        print(self.map_api_server, self.map_params)
        return ImageQt.ImageQt(
            Image.open(BytesIO(requests.get(self.map_api_server, params=self.map_params).content)))

    def initUI(self):

        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        ## Изображение
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(QPixmap.fromImage(self.getImage()))
        menuBar = self.menuBar()
        # Creating menus using a QMenu object

        mapMenu = QMenu("&Map Style", self)
        menuBar.addMenu(mapMenu)

        self.schemeAction = QAction('Схема', self, checkable=True)
        self.schemeAction.setChecked(True)
        self.schemeAction.triggered.connect(self.schemeShow)
        mapMenu.addAction(self.schemeAction)

        self.hybridAction = QAction('Гибрид', self, checkable=True)
        self.hybridAction.setChecked(False)
        self.hybridAction.triggered.connect(self.hybridShow)
        mapMenu.addAction(self.hybridAction)

    def schemeShow(self):
        if self.hybridAction.isChecked():
            self.hybridAction.setChecked(False)
            self.map_params["l"] = "map"
            self.updateMap()

    def hybridShow(self):
        if self.schemeAction.isChecked():
            self.schemeAction.setChecked(False)
            self.map_params["l"] = "skl"
            self.updateMap()


    def keyPressEvent(self, event):
        if event.key() == 16777239:
            dx = float(self.map_params["spn"].split(",")[0]) + self.scroll_value
            self.map_params["spn"] = f"{dx},{dx}"
            self.updateMap()

        elif event.key() == 16777238:
            dx = float(self.map_params["spn"].split(",")[0]) - self.scroll_value
            if dx < 0: dx += self.scroll_value
            self.map_params["spn"] = f"{dx},{dx}"
            self.updateMap()

        elif event.key() == 16777234:  # left
            a, b = map(float, self.map_params['ll'].split(','))
            self.map_params['ll'] = f"{a - 0.0005 - float(self.map_params['spn'].split(',')[0])},{b}"
            self.updateMap()
        elif event.key() == 16777236:  # right
            a, b = map(float, self.map_params['ll'].split(','))
            self.map_params['ll'] = f"{a + 0.0005 + float(self.map_params['spn'].split(',')[0])},{b}"
            self.updateMap()
        elif event.key() == 16777235:  # up
            a, b = map(float, self.map_params['ll'].split(','))
            self.map_params['ll'] = f"{a},{b + 0.0005 + float(self.map_params['spn'].split(',')[0])}"
            self.updateMap()
        elif event.key() == 16777237:  # down
            a, b = map(float, self.map_params['ll'].split(','))
            self.map_params['ll'] = f"{a},{b - 0.0005 - float(self.map_params['spn'].split(',')[0])}"
            self.updateMap()

    def updateMap(self):
        self.getImage()
        self.image.setPixmap(QPixmap.fromImage(self.getImage()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
