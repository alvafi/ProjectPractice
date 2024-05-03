from TestClasses.Answer import Answer
from TestClasses.Test import Test
from User import User
from UserInfo import UserInfo
from TestClasses.Bank import Bank
from TestClasses.Task import Task
from TestClasses.Kit import Kit
from database import Database
from random import sample

class Interface:

    # Добавление теста
    def add_test(self, kit: Kit, test_name: str, task_amount: int) -> Test | None:
        tasks_not_in_tests = kit.GetTaskNotInTests()

        if task_amount > len(tasks_not_in_tests):
            print("Количество заданий для теста больше, чем количество имеющихся заданий")
            return

        tasks_for_test = sample(tasks_not_in_tests, task_amount)
        test_id, error = Database().add_data_test(kit.GetId(), test_name)
        if test_id is None:
            print(error)
            return None

        id_of_tasks_for_test = [task.GetId() for task in tasks_for_test]
        is_updated, error = Database().update_task_tests_id(id_of_tasks_for_test, test_id)
        if not is_updated:
            print(error)
            return None

        for task in tasks_for_test:
            task.SetTestId(test_id)

        new_test = Test(test_id, test_name, tasks_for_test)
        kit.AddTest(new_test)
        return new_test

    # Добавление банка тестов
    def add_bank(self, user: User, bank_name: str) -> Bank | None:
        bank_id, error = Database().add_data_bank(user.GetId(), bank_name)
        if bank_id is None:
            print(error)
            return None

        new_bank = Bank(bank_id, bank_name)
        return new_bank

    # Добавление набора
    def add_kit(self, bank: Bank, kit_name: str) -> Kit | None:
        kit_id, error = Database().add_data_kit(bank.GetId(), kit_name)
        if kit_id is None:
            print(error)
            return None

        new_kit = Kit(kit_id, kit_name)
        bank.AddKit(new_kit)
        return new_kit

    # Добавление задания
    def add_task(self, kit: Kit, question_text: str) -> Task | None:
        task_id, error = Database().add_data_task(kit.GetId(), None, question_text)
        if task_id is None:
            print(error)
            return None

        new_task = Task(task_id, None, question_text, [])
        kit.AddTask(new_task)
        return new_task

    # Добавление ответа
    def add_answer(self, task: Task, answer_text: str, is_right: bool) -> Answer | None:
        answer_id, error = Database().add_data_answer(task.GetId(), answer_text, is_right)
        if answer_id is None:
            print(error)
            return None

        new_answer = Answer(answer_id, answer_text, is_right)
        task.AddAnswer(new_answer)
        return new_answer

    # Редактирование имени банка тестов
    def edit_bank_name(self, bank : Bank, new_bank_name : str):
        is_updated, error = Database().update_bank_name(bank.GetId(), new_bank_name)
        if not is_updated:
            print(error)
            return False

        bank.SetName(new_bank_name)
        return True

    # Редактирование имени набора
    def edit_kit_name(self, kit : Kit, new_kit_name : str):
        is_updated, error = Database().update_kit_name(kit.GetId(), new_kit_name)
        if not is_updated:
            print(error)
            return False

        kit.SetName(new_kit_name)
        return True

    # Редактирование имени теста
    def edit_test_name(self, test : Test, new_test_name : str):
        is_updated, error = Database().update_test_name(test.GetId(), new_test_name)
        if not is_updated:
            print(error)
            return False

        test.SetName(new_test_name)
        return True

    # Редактирование вопроса
    def edit_task_question(self, task : Task, new_task_question : str):
        is_updated, error = Database().update_task_question(task.GetId(), new_task_question)
        if not is_updated:
            print(error)
            return False

        task.SetQuestion(new_task_question)
        return True

    # Редактирование ответа и правильности ответа
    def edit_answer(self, answer : Answer, new_answer_text : str, new_is_right : bool):
        is_updated, error = Database().update_answer(answer.GetId(), new_answer_text, new_is_right)
        if not is_updated:
            print(error)
            return False

        answer.SetAnswerText(new_answer_text)
        answer.SetIsRight(new_is_right)
        return True
