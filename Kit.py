import Test

class Kit:
    def __init__(self, kit_id : int, name : str) -> None:
        self.__kit_id = kit_id
        self.__name = name
        self.__tests = []
        self.__tasks = []

    def GetId(self) -> int:
        return self.__kit_id
    
    def AddTest(self, test : Test) -> None:
        self.__tests.append(test)
        for task in test:
            self.__tasks.append(task)

    def GetName(self) -> str:
        return self.__name
    
    def GetTests(self) -> list[Test.Test]:
        return self.__tests

    def SetName(self, new_kit_name : str) -> None:
        self.__name = new_kit_name