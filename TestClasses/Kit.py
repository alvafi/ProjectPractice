from TestClasses.Test import Test
from TestClasses.Task import Task

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

    def AddTask(self, task : Task) -> None:
        self.__tasks.append(task)

    def GetName(self) -> str:
        return self.__name
    
    def GetTests(self) -> list[Test]:
        return self.__tests

    def GetTasks(self) -> list[Task]:
        return self.__tasks

    def GetTasksInTests(self) -> list[Task]:
        return sum([test.GetTasks() for test in self.GetTests()], [])

    def GetTaskNotInTests(self) -> list[Task]:
        return [task for task in self.GetTasks() if task not in self.GetTasksInTests()]

    def SetName(self, new_kit_name : str) -> None:
        self.__name = new_kit_name