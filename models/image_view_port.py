import copy
import logging
import cv2
import numpy as np
from enum import Enum
from PyQt6.QtGui import QCursor

import pyqtgraph as pg
from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtWidgets import QFileDialog

from models.image import Image, load_image_from_file_name


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
            self, window, image_original_viewer, image_component_viewer, mode_combo_box,
    ) -> None:
        self.image: Image = None

        self.window = window

        self.image_original_viewer = image_original_viewer
        self.image_original_viewer.showAxes(False)
        self.image_original_viewer.invertY(True)
        self.image_original_viewer.setLimits(xMin=0, xMax=1000, yMin=0, yMax=1000)

        self.image_component_viewer = image_component_viewer
        self.image_component_viewer.showAxes(False)
        self.image_component_viewer.setLimits(xMin=0, xMax=1000, yMin=0, yMax=1000)

        self.component_viewer_mode: ComponentViewMode = ComponentViewMode.MAGNITUDE
        self.mode_combo_box = mode_combo_box
        for mode in ComponentViewMode:
            self.mode_combo_box.addItem(mode.name.capitalize())
        self.component_result: np.ndarray = np.zeros((1000, 1000))
        self.roi = None

        self.mouse_pressed = False
        self.last_x, self.last_y = None, None

        # set original images brightness and contrast
        self.original_brightness = 255
        self.original_contrast = 127

        # set initial brightness and contrast
        self.brightness = 255
        self.contrast = 127


        self._initialize_slots()

    def _initialize_slots(self) -> None:
        self.image_original_viewer.mouseDoubleClickEvent = self._open_image
        self.mode_combo_box.currentIndexChanged.connect(self._on_combobox_changed)

        # Connect mouse events to custom functions
        self.image_original_viewer.scene().sigMouseClicked.connect(self.on_plot_click)
        self.image_original_viewer.scene().sigMouseMoved.connect(self.on_plot_move)
    def on_plot_click(self, event):
        # Set the mouse_pressed flag to True when the mouse button is pressed
        self.mouse_pressed = not self.mouse_pressed
        self.image_original_viewer.setCursor(QCursor(Qt.CursorShape.CrossCursor))

    def on_plot_move(self, event):
        # Print the x and y coordinates only if the mouse button is pressed
        if self.mouse_pressed:
            self.image_original_viewer.setCursor(QCursor(Qt.CursorShape.CrossCursor))
            pos = event
            x, y = pos.x(), pos.y()

            # set initial x, y
            if self.last_x is None:
                self.last_x, self.last_y = x, y

            new_image = copy.deepcopy(self.image)

            # change in x-axis changes the brightness
            if abs(x - self.last_x) > 10:
                new_image.image_array += int(x) // 20
                logging.info(
                    f"Change in Brightness with {x // 10} degrees"
                )
                self.image_original_viewer.addItem(pg.ImageItem(new_image.image_array))
                self.last_x = x

            # change in y-axis changes the contrast
            elif abs(y - self.last_y) > 10:
                new_image.image_array *= int(y) // 20
                logging.info(
                    f"Change in Contrast with {y // 10} degrees"
                )
                self.image_original_viewer.addItem(pg.ImageItem(new_image.image_array))
                self.last_y = y

        else:
            self.image_original_viewer.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

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

    def get_boundaries(self) -> tuple:
        if self.roi is None or self.image is None:
            return None

        pos = self.roi.pos()
        size = self.roi.size()
        x_start = int(pos[0])
        y_start = int(pos[1])
        x_end = int(pos[0] + size[0])
        y_end = int(pos[1] + size[1])

        return (x_start, x_end, y_start, y_end)

    @pyqtSlot()
    def _open_image(self, _) -> None:
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self.window, "Open Image", "", "Images (*.png *.jpg *.bmp *.gif)"
        )

        if file_path:
            self.image = load_image_from_file_name(file_name=file_path)
            logging.info(
                f"Opened image: {file_path} - with size: {self.image.image_array.shape}"
            )
            self._render_image()
        else:
            logging.error("There was an error loading the image")

