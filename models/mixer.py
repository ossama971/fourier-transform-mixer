from enum import Enum

from models.image_view_port import ComponentViewMode


class ImageNumber(Enum):
    """
    Enum for different component view modes.
    """

    Image1 = 0
    Image2 = 1
    Image3 = 2
    Image4 = 3



class OutputPanel:
    def __init__(self, window, output_viewer, first_image, second_image, first_image_mode_compo_box,
                 second_image_mode_compo_box, component1_weight_slider, component2_weight_slider):
        self.window = window
        self.output_viewer = output_viewer
        self.first_image = first_image
        self.second_image = second_image
        self.first_image_mode_compo_box = first_image_mode_compo_box
        self.second_image_mode_compo_box = second_image_mode_compo_box
        self.component1_weight_slider = component1_weight_slider
        self.component2_weight_slider = component2_weight_slider

        for mode in ComponentViewMode:
            self.first_image_mode_compo_box.addItem(mode.name.capitalize())
            self.second_image_mode_compo_box.addItem(mode.name.capitalize())

        for image in ImageNumber:
            self.first_image.addItem(image.name.capitalize())
            self.second_image.addItem(image.name.capitalize())
        self._initialize_slots()

    def _initialize_slots(self) -> None:
        pass
        # self.image_original_viewer.mousePressEvent = self._open_image
        # self.mode_combo_box.currentIndexChanged.connect(self._on_combobox_changed)
