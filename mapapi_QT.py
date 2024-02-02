import sys
from io import BytesIO

import requests
from PIL import Image, ImageQt
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self, map_api_server, map_params):
        super().__init__()
        self.map_api_server = map_api_server
        self.map_params = map_params
        self.scroll_value = 0.01
        self.initUI()

    def getImage(self):
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

    def keyPressEvent(self, event):
        if event.key() == 16777239:
            dx = float(self.map_params["spn"].split(",")[0]) + self.scroll_value
            self.map_params["spn"] = f"{dx},{dx}"
            self.getImage()
            self.image.setPixmap(QPixmap.fromImage(self.getImage()))
        if event.key() == 16777238:
            dx = float(self.map_params["spn"].split(",")[0]) - self.scroll_value
            if dx < 0: dx += self.scroll_value
            self.map_params["spn"] = f"{dx},{dx}"
            self.getImage()
            self.image.setPixmap(QPixmap.fromImage(self.getImage()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
