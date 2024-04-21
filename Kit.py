import Test

class Kit:
    def __init__(self, name : str) -> None:
        self.__name = name
        self.__tests = []
        self.__tasks = []
    
    def AddTest(self, test : Test) -> None:
        self.__tests.append(test)
        for task in test:
            self.__tasks.append(task)

    def GetName(self) -> str:
        return self.__name
    
    def GetTests(self) -> list[Test.Test]:
        return self.__tests