import sys
from io import BytesIO

import requests
from PIL import Image, ImageQt
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self, response):
        super().__init__()
        self.getImage(response)
        self.initUI()

    def getImage(self, response):
        self.img = ImageQt.ImageQt(Image.open(BytesIO(response.content)))

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(QPixmap.fromImage(self.img))

    def keyPressEvent(self, event):
        print(event.key() == 16777239)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
