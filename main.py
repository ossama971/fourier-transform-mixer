import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
import pyqtgraph as pg

from models.image_view_port import ImageViewPort

uiclass, baseclass = pg.Qt.loadUiType("mainwindow.ui")


class MainWindow(uiclass, baseclass):
    def __init__(self):
        super().__init__()

        # Window and UI configurations
        self.setupUi(self)
        self.setWindowTitle("Fourier Transform Mixer")
        self.show()

        # Initialize states, signals, and slots
        self._initialize_image_viewers()
        self._initialize_slots()

    def _initialize_image_viewers(self):
        self.images = [
            ImageViewPort(
                window=self,
                image_original_viewer=self.image_original_1,
                image_component_viewer=self.image_component_1,
                mode_combo_box=self.image_combo_1,
            ),
            ImageViewPort(
                window=self,
                image_original_viewer=self.image_original_2,
                image_component_viewer=self.image_component_2,
                mode_combo_box=self.image_combo_2,
            ),
            ImageViewPort(
                window=self,
                image_original_viewer=self.image_original_3,
                image_component_viewer=self.image_component_3,
                mode_combo_box=self.image_combo_3,
            ),
            ImageViewPort(
                window=self,
                image_original_viewer=self.image_original_4,
                image_component_viewer=self.image_component_4,
                mode_combo_box=self.image_combo_4,
            ),
        ]

    def _initialize_slots(self) -> None:
        self.region_slider.valueChanged.connect(self._region_slider_value_changed)

    def _region_slider_value_changed(self, value) -> None:
        for image_view_port in self.images:
            image_view_port.draw_region_square(scale=(value / 100))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()


if __name__ == "__main__":
    main()
