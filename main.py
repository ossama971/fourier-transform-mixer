import os

# Suppress Qt logging
os.environ["QT_LOGGING_RULES"] = "*=false"
import sys
import logging
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication

# Import models
from models.image_view_port import ImageViewPort
from models.output_panel import OutputPanel, OutputModes
from models.mixer import Mixer, MixModes

uiclass, baseclass = pg.Qt.loadUiType("views/mainwindow.ui")


class MainWindow(uiclass, baseclass):
    def __init__(self):
        super().__init__()

        # Window and UI configurations
        self.setupUi(self)
        self.setWindowTitle("Fourier Transform Mixer")
        self.show()

        # App State
        self.current_mode = MixModes.REAL_IMAGINARY
        self.current_output = OutputModes.OUTPUT_1
        self._notify_combobox_observers()
        self.roi_inner_outer = 'Inner'

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
                output_viewer=self.image_output_1,
            ),
            OutputPanel(
                output_viewer=self.image_output_2,
            ),
        ]

    def _notify_combobox_observers(self):
        observers = [
            self.image_comp_1,
            self.image_comp_2,
            self.image_comp_3,
            self.image_comp_4,
        ]
        for combobox in observers:
            combobox.clear()
            if self.current_mode == MixModes.MAG_PHASE:
                combobox.addItems(["Magnitude", "Phase"])
            else:
                combobox.addItems(["Real", "Imaginary"])

    def _initialize_slots(self) -> None:
        self.region_slider.valueChanged.connect(self._region_slider_value_changed)
        self.output_btn.clicked.connect(self._display_mixer_output)
        self.image_1_weight_slider.valueChanged.connect(
            self._output_slider_value_changed
        )
        self.image_2_weight_slider.valueChanged.connect(
            self._output_slider_value_changed
        )
        self.image_3_weight_slider.valueChanged.connect(
            self._output_slider_value_changed
        )
        self.image_4_weight_slider.valueChanged.connect(
            self._output_slider_value_changed
        )

        # Output mode radio buttons
        self.output_rad_1.toggled.connect(self._on_output_mode_radio_button_toggled)
        self.output_rad_2.toggled.connect(self._on_output_mode_radio_button_toggled)

        # Mixing mode radio buttons
        self.mode_rad_1.toggled.connect(self._on_mode_radio_button_toggled)
        self.mode_rad_2.toggled.connect(self._on_mode_radio_button_toggled)

        # ROI mode radio buttons
        self.inner_rad.toggled.connect(self._on_roi_radio_button_toggled)
        self.outer_rad.toggled.connect(self._on_roi_radio_button_toggled)

    def _on_roi_radio_button_toggled(self):
        # Get the radio button that triggered the event
        # and change state accordingly
        sender = self.sender()

        if sender.isChecked():
            self.roi_inner_outer = sender.text()
            logging.info(f"ROI is {self.roi_inner_outer} region")

        self._display_mixer_output()

    def _on_mode_radio_button_toggled(self):
        # Get the radio button that triggered the event
        # and change state accordingly
        sender = self.sender()

        if sender.isChecked():
            if sender.text() == "Real and Imaginary":
                self.current_mode = MixModes.REAL_IMAGINARY
            else:
                self.current_mode = MixModes.MAG_PHASE
        self._notify_combobox_observers()

    def _on_output_mode_radio_button_toggled(self):
        # Get the radio button that triggered the event
        # and change state accordingly
        sender = self.sender()

        if sender.isChecked():
            if sender.text() == "Output 1":
                self.current_output = OutputModes.OUTPUT_1
            else:
                self.current_output = OutputModes.OUTPUT_2
        print(self.current_output)

    def _region_slider_value_changed(self, value) -> None:
        for image_view_port in self.images:
            image_view_port.draw_region_square(scale=(value / 100))

        self._display_mixer_output()

    def _output_slider_value_changed(self, value):
        self._display_mixer_output()

    def _get_curr_region(self):
        print('curr_region:',self.images[0].get_boundries())
        return self.images[0].get_boundries()

    def _display_mixer_output(self):
        logging.info(f"Slicing region is {self.region_slider.value()}")
        current_output_port = (
            self.image_output_1
            if self.current_output == OutputModes.OUTPUT_1
            else self.image_output_2
        )
        mixer = Mixer(
            window=self,
            images=self.images,
            output_port=current_output_port,
            region=self._get_curr_region(),
            mix_mode=self.current_mode,
            roi_inner_outer=self.roi_inner_outer
        )
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
