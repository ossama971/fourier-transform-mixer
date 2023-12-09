from enum import Enum
import numpy as np
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QFileDialog
import pyqtgraph as pg
from models.image import Image

class ComponentViewMode(Enum):
    """
    Enum for different component view modes.
    """


    MAGNITUDE = 0
    PHASE = 1
    REAL = 2
    IMAGINARY = 3


class ImageViewPort:
    def __init__(
        self, window, image_original_viewer, image_component_viewer, mode_combo_box
    ) -> None:
        self.image: Image = None

        self.window = window

        self.image_original_viewer = image_original_viewer
        self.image_original_viewer.showAxes(False)
        self.image_original_viewer.invertY(True)

        self.image_component_viewer = image_component_viewer
        self.image_component_viewer.showAxes(False)
        self.image_component_viewer.invertY(True)

        self.component_viewer_mode: ComponentViewMode = ComponentViewMode.MAGNITUDE
        self.mode_combo_box = mode_combo_box
        for mode in ComponentViewMode:
            self.mode_combo_box.addItem(mode.name.capitalize())
        self.component_result: np.ndarray
        self.roi = None

        self._initialize_slots()

    def _initialize_slots(self) -> None:
        self.image_original_viewer.mousePressEvent = self._open_image
        self.mode_combo_box.currentIndexChanged.connect(self._on_combobox_changed)

    def _on_combobox_changed(self, index) -> None:
        self.component_viewer_mode = ComponentViewMode(index)
        print(self.component_viewer_mode)
        self._render_component_for_current_image()

    def _render_image(self) -> None:
        self.image_original_viewer.addItem(pg.ImageItem(self.image.image_array))
        self._render_component_for_current_image()

    def _render_component_for_current_image(self) -> None:
        if self.component_viewer_mode == ComponentViewMode.MAGNITUDE:
            self.component_result = 20 * np.log(self.image.magnitude.T)
        elif self.component_viewer_mode == ComponentViewMode.PHASE:
            self.component_result = self.image.phase.T
        elif self.component_viewer_mode == ComponentViewMode.REAL:
            self.component_result = 20 * np.log(self.image.real.T)
        elif self.component_viewer_mode == ComponentViewMode.IMAGINARY:
            self.component_result = self.image.imaginary.T
        else:
            self.component_result = self.image.image_array
        self.image_component_viewer.addItem(pg.ImageItem(self.component_result))
        self.draw_region_square(scale=1.0)

    def draw_region_square(self, scale: float) -> None:
        if self.component_result.any():
            image_width, image_height = self.component_result.shape[:2]
            center_x = image_width // 2
            center_y = image_height // 2
            rect_width = image_height * scale
            rect_height = image_width * scale
            if self.roi is not None:
                self.image_component_viewer.removeItem(self.roi)

            self.roi = pg.ROI(
                [center_x - rect_width / 2, center_y - rect_height / 2],
                [rect_width, rect_height],
                pen=pg.mkPen("r", width=2),
            )
            self.image_component_viewer.addItem(self.roi)

    @pyqtSlot()
    def _open_image(self, _) -> None:
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self.window, "Open Image", "", "Images (*.png *.jpg *.bmp *.gif)"
        )

        if file_path:
            self.image = Image(file_name=file_path)
            self._render_image()

