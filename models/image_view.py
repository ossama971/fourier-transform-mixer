from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QFileDialog
import pyqtgraph as pg
from models.image import Image


class ImageViewPort:
    def __init__(self, window, image_original_viewer, image_component_viewer) -> None:
        self.image: Image = None

        self.window = window

        self.image_original_viewer = image_original_viewer
        self.image_original_viewer.showAxes(False)
        self.image_original_viewer.invertY(True)

        self.image_component_viewer = image_component_viewer
        self.image_component_viewer.showAxes(False)
        self.image_component_viewer.invertY(True)

        self._initialize_image_slots()

    def _initialize_image_slots(self):
        self.image_original_viewer.mousePressEvent = self._open_image

    @pyqtSlot()
    def _open_image(self, _):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self.window, "Open Image", "", "Images (*.png *.jpg *.bmp *.gif)"
        )

        if file_path:
            self.image = Image(file_name=file_path)
            self.image_original_viewer.addItem(pg.ImageItem(self.image.image_array))
