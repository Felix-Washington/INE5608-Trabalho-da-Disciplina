

class Question:
    def __init__(self, content, topic):
        self.__content = content
        self.__topic = topic
        self.__used = False


    @property
    def used(self):
        return self.__used    

    @used.setter
    def used(self, used):
        if isinstance(used, bool):
            self.__used = used


    @property
    def content(self):
        return self.__content
    

    @property
    def topic(self):
        return self.__topic
    
