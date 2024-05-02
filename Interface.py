import ProjectPractice.TestClasses.Answer as Answer
import ProjectPractice.TestClasses.Test as Test
import User
import UserInfo
import ProjectPractice.TestClasses.Bank as Bank
import ProjectPractice.TestClasses.Task as Task
import ProjectPractice.TestClasses.Kit as Kit
import database

class Interface:

    # Редактирование имени банка тестов
    def edit_bank_name(self, user : User.User, bank : Bank.Bank, new_bank_name : str):
        bank.SetName(new_bank_name)
        database.Database().update_bank_name(user.GetId(), bank.GetId(), new_bank_name)

    # Редактирование имени набора
    def edit_kit_name(self, kit : Kit.Kit, new_kit_name : str):
        kit.SetName(new_kit_name)
        database.Database().update_kit_name(kit.GetId(), new_kit_name)

    # Редактирование имени теста
    def edit_test_name(self, test : Test.Test, new_test_name : str):
        test.SetName(new_test_name)
        database.Database().update_test_name(test.GetId(), new_test_name)

    # Редактирование вопроса
    def edit_task_question(self, task : Task.Task, new_task_question : str):
        task.SetHeadText(new_task_question)
        database.Database().update_test_question(task.GetId(), new_task_question)

    # Редактирование ответа и правильности ответа
    def edit_answer(self, answer : Answer.Answer, new_answer_text : str, new_is_right : bool):
        answer.SetAnswerText(new_answer_text)
        answer.SetIsRight(new_is_right)
        database.Database().update_answer(answer.GetId(), answer.GetText(), answer.IsRight())
