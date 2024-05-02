import ProjectPractice.TestClasses.Task as Task

class Test:
    def __init__(self, test_id : int, name : str) -> None:
        self.__test_id = test_id
        self.__name = name
        self.__tasks = []

    def GetId(self) -> int:
        return self.__test_id

    def AddTask(self, task : Task) -> None:
        self.__tasks.append(task)

    def GetName(self) -> str:
        return self.__name
    
    def GetTasks(self) -> list[Task.Task]:
        return self.__tasks

    def SetName(self, new_test_name : str) -> None:
        self.__name = new_test_name