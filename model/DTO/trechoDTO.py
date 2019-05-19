
class trechoDTO:
    def __init__(self,trecho,name=""):
        self.trecho = trecho
        self.name = list(name)

        @property
        def trecho(self):
            return self.__trecho

        @property
        def name(self):
            return self.__name

        @name.setter
        def name(self, val):
            self.__name.append(val)
