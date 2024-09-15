

class Answer:
    def __init__(self, content, topic):
        self.__content = content
        self.__topic = topic

    @property
    def content(self):
        return self.__content

    @property
    def topic(self):
        return self.__topic