from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtGui import QPixmap
from utils.image_utils import grayscale_image


class Image:
    def __init__(self, window, image_original_viewer) -> None:
        self.window = window
        self.image_original_viewer = image_original_viewer
        self._initialize_image_slots()

    def _initialize_image_slots(self):
        self.image_original_viewer.mousePressEvent = self._open_image

    @pyqtSlot()
    def _open_image(self, event):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self.window, "Open Image", "", "Images (*.png *.jpg *.bmp *.gif)"
        )

        if file_path:
            original_pixmap = QPixmap(file_path)

            # Grayscale the image
            grayscale_pixmap = grayscale_image(original_pixmap)

            # Show the grey scaled image
            self.image_original_viewer.setPixmap(
                grayscale_pixmap.scaled(
                    self.image_original_viewer.size(),
                    # aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio,
                )
            )
