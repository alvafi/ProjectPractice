class Answer:
    def __init__(self, answer : str, is_right : bool) -> None:
        self.__answer = answer
        self.__is_right = is_right
    
    def GetText(self) -> str:
        return self.__answer
    
    def IsRight(self) -> bool:
        return self.__is_right

    def SetAnswerText(self, new_answer_text : str) -> None:
        self.__answer = new_answer_text

    def SetIsRight(self, new_is_right : bool) -> None:
        self.__is_right = new_is_right
