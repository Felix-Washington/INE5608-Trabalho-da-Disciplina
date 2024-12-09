

class Card:
    def __init__(self, options, question=-1):
        # Current selected question.
        self.__question = question

        # Card widget size.
        self.__width = 400
        self.__height = 600
        # Card is created with 4 options.
        self.__options = options

    @property
    def question(self):
        return self.__question

    @question.setter
    def question(self, question):
        self.__question = question

    @property
    def options(self):
        return self.__options

    @options.setter
    def options(self, options):
        self.__options = options

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height
