class Position:
    def __init__(self, new_type, widget, image_path):
        super().__init__()
        self.__type = new_type
        # Used for Label
        self.__widget = widget
        self.__image = image_path

    @property
    def widget(self):
        return self.__widget

    @widget.setter
    def widget(self, widget):
        self.__widget = widget

    @property
    def type(self):
        return self.__type

    def new_type(self, new_type):
        self.__type = new_type

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, image):
        self.__image = image