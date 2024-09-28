

class Card:
    def __init__(self, questions, answers):
        self.__questions = questions
        self.__answers = answers

        self.__width = 400
        self.__height = 600

    @property
    def questions(self):
        return self.__questions

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def answers(self):
        return self.__answers
