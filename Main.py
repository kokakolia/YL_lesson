import sys
from io import BytesIO

from PyQt6.QtWidgets import QApplication

import geocoder
from mapapi_QT import Example

import requests
from PIL import Image

toponym_to_find = " ".join(sys.argv[1:])
ll, spn = geocoder.get_ll_span(toponym_to_find)
map_params = {
    "ll": ll,
    "spn": spn,
    "l": "map",
}
map_api_server = "http://static-maps.yandex.ru/1.x/"
app = QApplication(sys.argv)
map = Example(map_api_server, map_params)
map.show()
sys.exit(app.exec())
