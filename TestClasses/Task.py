import ProjectPractice.TestClasses.Answer as Answer

class Task:
    def __init__(self, task_id : int, head_text : str, answers : list[Answer.Answer]) -> None:
        self.__task_id = task_id
        self.__head_text = head_text
        self.__answers = answers

    def GetId(self) -> int:
        return self.__task_id
    
    def GetHeadName(self) -> str:
        return self.__head_text
    
    def GetAnswers(self) -> list[Answer.Answer]:
        return self.__answers

    def GetRightAnswers(self) -> list[Answer.Answer]:
        right_answers = []
        for answer in self.__answers:
            if answer.IsRight():
                right_answers.append(answer)

        return right_answers

    def SetHeadText(self, new_head_text : str) -> None:
        self.__head_text = new_head_text

    def DeleteAnswer(self, answer : Answer.Answer) -> None:
        self.__answers.remove(answer)
    
