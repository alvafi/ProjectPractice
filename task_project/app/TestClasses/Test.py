from TestClasses.Task import Task

class Test:
    def __init__(self, name : str) -> None:
        self.__name = name
        self.__tasks = []

    def AddTask(self, task : Task) -> None:
        self.__tasks.append(task)

    def GetName(self) -> str:
        return self.__name
    
    def GetTasks(self) -> list[Task]:
        return self.__tasks

    def SetName(self, new_test_name : str) -> None:
        self.__name = new_test_name