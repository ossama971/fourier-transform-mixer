import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow

from models.image import Image


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Window and UI configurations
        uic.loadUi("mainwindow.ui", self)
        self.setWindowTitle("Fourier Transform Mixer")
        self.show()

        # Initialize states, signals, and slots
        self._initialize_image_viewers()

    def _initialize_image_viewers(self):
        self.images = [
            Image(window=self, image_original_viewer=self.image_original_1),
            Image(window=self, image_original_viewer=self.image_original_2),
            Image(window=self, image_original_viewer=self.image_original_3),
            Image(window=self, image_original_viewer=self.image_original_4),
        ]


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()


if __name__ == "__main__":
    main()
