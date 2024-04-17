import Answer

class Task:
    def __init__(self, head_text : str, answers : list[Answer.Answer]) -> None:
        self.__head_text = head_text
        self.__answers = answers
    
    def GetHeadName(self) -> str:
        return self.__head_text
    
    def GetAnswers(self) -> list[Answer.Answer]:
        return self.__answers

    def GetRightAnswers(self) -> list[Answer.Answer]:
        rigth_answers = []
        for answer in self.__answers:
            if answer.IsRight():
                rigth_answers.append(answer)

        return rigth_answers
    
