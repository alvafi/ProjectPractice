class Answer:
    def __init__(self, answer : str, is_right : bool) -> None:
        self.__answer = answer
        self.__is_right = is_right
    
    def GetText(self) -> str:
        return self.__answer
    
    def IsRight(self) -> bool:
        return self.__is_right
