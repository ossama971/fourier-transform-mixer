import logging
import cv2
import numpy as np
import pyqtgraph as pg

from enum import Enum
from models.image_view_port import ComponentViewMode


class OutputModes(Enum):
    """
    Enum for different output modes.
    """

    OUTPUT_1 = 1
    OUTPUT_2 = 2


class OutputPanel:
    def __init__(
        self,
        output_viewer,
    ):
        self.output_viewer = output_viewer
        self.output_viewer.showAxes(False)
        self.output_viewer.rotate(90)

        self._initialize_slots()

    def _initialize_slots(self) -> None:
        pass
