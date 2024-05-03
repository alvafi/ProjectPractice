from TestClasses.Answer import Answer

class Task:
    def __init__(self, task_id : int, test_id : int | None, question_text : str, answers : list[Answer]) -> None:
        self.__task_id = task_id
        self.__test_id = test_id
        self.__question_text = question_text
        self.__answers = answers

    def GetId(self) -> int:
        return self.__task_id
    
    def GetQuestion(self) -> str:
        return self.__question_text
    
    def GetAnswers(self) -> list[Answer]:
        return self.__answers

    def GetTestId(self) -> int | None:
        return self.__test_id

    def GetRightAnswers(self) -> list[Answer]:
        right_answers = []
        for answer in self.__answers:
            if answer.IsRight():
                right_answers.append(answer)

        return right_answers

    def AddAnswer(self, answer : Answer):
        self.__answers.append(answer)

    def SetQuestion(self, new_question_text : str) -> None:
        self.__question_text = new_question_text

    def SetAnswers(self, answers : list[Answer]):
        self.__answers = answers

    def SetTestId(self, new_test_id : int) -> None:
        self.__test_id = new_test_id

    def DeleteAnswer(self, answer : Answer) -> None:
        self.__answers.remove(answer)
    
