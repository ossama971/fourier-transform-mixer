import os

# Suppress Qt logging
os.environ["QT_LOGGING_RULES"] = "*=false"
import sys
import logging
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication

# Import models
from models.image_view_port import ImageViewPort
from models.output_panel import OutputPanel
from models.mixer import Mixer

uiclass, baseclass = pg.Qt.loadUiType("views/mainwindow.ui")


class MainWindow(uiclass, baseclass):
    def __init__(self):
        super().__init__()

        # Window and UI configurations
        self.setupUi(self)
        self.setWindowTitle("Fourier Transform Mixer")
        self.show()

        # Initialize states, signals, and slots
        self._initialize_image_viewers()
        self._initialize_output_viewers()
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

    def _initialize_output_viewers(self):
        self.output_ports = [
            OutputPanel(
                window=self,
                output_viewer=self.image_output_1,
                first_image_combo_box=self.image_1_output_1,
                second_image_combo_box=self.image_2_output_1,
                first_image_mode_compo_box=self.image_1_component_output_1,
                second_image_mode_compo_box=self.image_2_component_output_1,
                component1_weight_slider=self.image_1_output_1_slider,
                component2_weight_slider=self.image_2_output_1_slider,
            ),
            OutputPanel(
                window=self,
                output_viewer=self.image_output_2,
                first_image_combo_box=self.image_1_output_2,
                second_image_combo_box=self.image_2_output_2,
                first_image_mode_compo_box=self.image_1_component_output_2,
                second_image_mode_compo_box=self.image_2_component_output_2,
                component1_weight_slider=self.image_1_output_2_slider,
                component2_weight_slider=self.image_2_output_2_slider,
            ),
        ]

    def _initialize_slots(self) -> None:
        self.region_slider.valueChanged.connect(self._region_slider_value_changed)
        self.output_btn.clicked.connect(self._display_mixer_output)
        self.image_1_output_1_slider.valueChanged.connect(self._output_slider_value_changed)
        self.image_2_output_1_slider.valueChanged.connect(self._output_slider_value_changed)
        self.image_1_output_2_slider.valueChanged.connect(self._output_slider_value_changed)
        self.image_2_output_2_slider.valueChanged.connect(self._output_slider_value_changed)

    def _region_slider_value_changed(self, value) -> None:
        for image_view_port in self.images:
            image_view_port.draw_region_square(scale=(value / 100))

        self._display_mixer_output()

    def _output_slider_value_changed(self, value):
        self._display_mixer_output()

    def _get_curr_region(self):
        return self.images[0].get_boundries()

    def _display_mixer_output(self):
        logging.info(f"Slicing region is {self.region_slider.value()}")
        mixer = Mixer(window=self, region=self._get_curr_region())
        mixer.mix()


def main() -> None:
    logging.basicConfig(
        filename="example.log",
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logging.info("Program has started")

    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()


if __name__ == "__main__":
    main()
