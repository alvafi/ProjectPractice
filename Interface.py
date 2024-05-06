from TestClasses.Answer import Answer
from TestClasses.Test import Test
from User import User
from UserInfo import UserInfo
from TestClasses.Bank import Bank
from TestClasses.Task import Task
from TestClasses.Kit import Kit
from database import Database
from random import sample


# Добавление теста
def add_test(kit: Kit, test_name: str, task_amount: int) -> Test | None:
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
def add_bank(user: User, bank_name: str) -> Bank | None:
    bank_id, error = Database().add_data_bank(user.GetId(), bank_name)
    if bank_id is None:
        print(error)
        return None

    new_bank = Bank(bank_id, bank_name)
    return new_bank

# Добавление набора
def add_kit(dbase, bank_id, kit_name: str) -> Kit | None:
    kit_id, error = dbase.add_data_kit(bank_id, kit_name)
    if kit_id is None:
        return False
    return kit_id

# Добавление теста
def add_test(dbase, kit_id, test_name: str) -> Kit | None:
    test_id, error = dbase.add_data_test(kit_id, test_name)
    if test_id is None:
        return False
    return test_id

# Добавление задания
def add_task(dbase, kit_id, test_id, question_text: str) -> Task | None:
    task_id, error = dbase.add_data_task(kit_id, test_id, question_text)
    if task_id is None:
        return False
    return task_id

# Добавление ответа
def add_answer(dbase, task_id, answer_text: str, is_right: bool) -> Answer | None:
    answer_id, error = dbase.add_data_answer(task_id, answer_text, is_right)
    if answer_id is None:
        return False
    return answer_id

# Добавление содержимого набора в бд
def add_kit_content(dbase, kit : Kit, bank_id):
    # Добавление набора
    kit_id = add_kit(dbase, bank_id, kit.GetName())
    if not(kit_id):
        return False
    print(kit_id, "kit_id")

    # Добавление тестов
    for test in kit.GetTests():
        test_id = add_test(dbase, kit_id, test.GetName())
        if not(test_id):
            return False
        print(test_id, "test_id")
    
        # Добавление заданий
        for task in test.GetTasks():
            task_id = add_task(dbase, kit_id, test_id, task.GetQuestion())
            if not(task_id):
                return False
            print(task_id, "task_id")
            # Добавление ответа
            for answer in task.GetAnswers():
                answer_id = add_answer(dbase, task_id, answer.GetText(), answer.IsRight())
                if not(answer_id):
                    return False
                print(answer_id, "answer_id")
    return True


# Редактирование имени банка тестов
def edit_bank_name(bank : Bank, new_bank_name : str):
    is_updated, error = Database().update_bank_name(bank.GetId(), new_bank_name)
    if not is_updated:
        print(error)
        return False

    bank.SetName(new_bank_name)
    return True

# Редактирование имени набора
def edit_kit_name(kit : Kit, new_kit_name : str):
    is_updated, error = Database().update_kit_name(kit.GetId(), new_kit_name)
    if not is_updated:
        print(error)
        return False

    kit.SetName(new_kit_name)
    return True

# Редактирование имени теста
def edit_test_name(test : Test, new_test_name : str):
    is_updated, error = Database().update_test_name(test.GetId(), new_test_name)
    if not is_updated:
        print(error)
        return False

    test.SetName(new_test_name)
    return True

# Редактирование вопроса
def edit_task_question(task : Task, new_task_question : str):
    is_updated, error = Database().update_task_question(task.GetId(), new_task_question)
    if not is_updated:
        print(error)
        return False

    task.SetQuestion(new_task_question)
    return True

# Редактирование ответа и правильности ответа
def edit_answer(answer : Answer, new_answer_text : str, new_is_right : bool):
    is_updated, error = Database().update_answer(answer.GetId(), new_answer_text, new_is_right)
    if not is_updated:
        print(error)
        return False

    answer.SetAnswerText(new_answer_text)
    answer.SetIsRight(new_is_right)
    return True
