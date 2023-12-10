import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
import pyqtgraph as pg

from models.image_view_port import ImageViewPort
from models.mixer import OutputPanel

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
            # ImageViewPort(
            #     window=self,
            #     image_original_viewer=self.image_original_3,
            #     image_component_viewer=self.image_component_3,
            #     mode_combo_box=self.image_combo_3,
            # ),
            # ImageViewPort(
            #     window=self,
            #     image_original_viewer=self.image_original_4,
            #     image_component_viewer=self.image_component_4,
            #     mode_combo_box=self.image_combo_4,
            # ),
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

    def _region_slider_value_changed(self, value) -> None:
        for image_view_port in self.images:
            image_view_port.draw_region_square(scale=(value / 100))

        # todo need to change calling place
        self._display_mixer_output()

    # todo to be continued
    def _display_mixer_output(self):
        img_idx_dictionary = {"Image1": 0, "Image2": 1, "Image3": 2, "Image4": 3}

        image_indices = {
            "output_1": [
                img_idx_dictionary[self.image_1_output_1.currentText()],
                img_idx_dictionary[self.image_2_output_1.currentText()],
            ],
            "output_2": [
                img_idx_dictionary[self.image_1_output_2.currentText()],
                img_idx_dictionary[self.image_2_output_2.currentText()],
            ],
        }

        images = {
            "output_1": [
                self.images[image_indices["output_1"][0]].image,
                self.images[image_indices["output_1"][1]].image,
            ],
            "output_2": [
                self.images[image_indices["output_2"][0]].image,
                self.images[image_indices["output_2"][1]].image,
            ],
        }

        for output in ["output_1", "output_2"]:
            if all(image is not None for image in images[output]):
                self._process_images(output, images[output])

    def _process_images(self, output, images):
        output_idx = int(output.split("_")[-1]) - 1
        component_1 = self.__getattribute__(f"image_1_component_{output}").currentText()
        component_2 = self.__getattribute__(f"image_2_component_{output}").currentText()

        if component_1 == "Magnitude" and component_2 == "Phase":
            self.output_ports[output_idx].reconstruct_image_using_magnitude_phase(
                *images
            )
        elif component_1 == "Phase" and component_2 == "Magnitude":
            self.output_ports[output_idx].reconstruct_image_using_magnitude_phase(
                *reversed(images)
            )
        elif component_1 == "Real" and component_2 == "Imaginary":
            self.output_ports[output_idx].reconstruct_image_using_real_imaginary(
                *images
            )
        elif component_1 == "Imaginary" and component_2 == "Real":
            self.output_ports[output_idx].reconstruct_image_using_real_imaginary(
                *reversed(images)
            )


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()


if __name__ == "__main__":
    main()
