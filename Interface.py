from TestClasses.Answer import Answer
from TestClasses.Test import Test
from User import User
from TestClasses.Bank import Bank
from TestClasses.Task import Task
from TestClasses.Kit import Kit
from database import Database
from random import sample


# Создание теста для уже существующих заданий
def make_test(dbase, kit_id, test_name: str, task_amount: int):
    tasks = dbase.get_tasks_by_kit_id_where_test_id_is_null(kit_id)

    if isinstance(tasks, bool):
        print("Отсутствуют свободные задания для теста или ошибка получения данных")
        return False

    if task_amount > len(tasks):
        print("Количество заданий для теста больше, чем количество имеющихся заданий")
        return False

    tasks_id_for_test = sample([task_id[0] for task_id in tasks], task_amount)
    print(tasks_id_for_test)

    test_id, error = dbase.add_data_test(kit_id, test_name)
    if test_id is None:
        print(error)
        return False

    is_updated, error = Database().update_task_tests_id(tasks_id_for_test, test_id)
    if not is_updated:
        print(error)
        return False

    return test_id

# Добавление банка тестов
def add_bank(dbase, user_id, bank_name: str):
    bank_id, error = dbase.add_data_bank(user_id, bank_name)
    if bank_id is None:
        print(error)
        return False

    return bank_id

# Добавление набора
def add_kit(dbase, bank_id, kit_name: str):
    kit_id, error = dbase.add_data_kit(bank_id, kit_name)
    if kit_id is None:
        return False
    return kit_id

# Добавление теста при вводе
def add_test(dbase, kit_id, test_name: str):
    test_id, error = dbase.add_data_test(kit_id, test_name)
    if test_id is None:
        return False
    return test_id

# Добавление задания
def add_task(dbase, kit_id, test_id, question_text: str):
    task_id, error = dbase.add_data_task(kit_id, test_id, question_text)
    if task_id is None:
        return False
    return task_id

# Добавление ответа
def add_answer(dbase, task_id, answer_text: str, is_right: bool):
    answer_id, error = dbase.add_data_answer(task_id, answer_text, is_right)
    if answer_id is None:
        return False
    return answer_id

# Добавление содержимого набора в бд
def add_kit_content(dbase, kit: Kit, bank_id):
    # Добавление набора
    kit_id = add_kit(dbase, bank_id, kit.GetName())
    if not (kit_id):
        return False

    # Добавление тестов
    for test in kit.GetTests():
        test_id = add_test(dbase, kit_id, test.GetName())
        if not (test_id):
            return False

        # Добавление заданий
        for task in test.GetTasks():
            task_id = add_task(dbase, kit_id, test_id, task.GetQuestion())
            if not (task_id):
                return False
            # Добавление ответа
            for answer in task.GetAnswers():
                answer_id = add_answer(dbase, task_id, answer.GetText(), answer.IsRight())
                if not (answer_id):
                    return False
    return True

def add_kit_content_to_existing_kit(dbase, kit: Kit, kit_id):
    # Добавление тестов
    for test in kit.GetTests():
        test_id = add_test(dbase, kit_id, test.GetName())
        if not (test_id):
            return False

        # Добавление заданий
        for task in test.GetTasks():
            task_id = add_task(dbase, kit_id, test_id, task.GetQuestion())
            if not (task_id):
                return False
            # Добавление ответа
            for answer in task.GetAnswers():
                answer_id = add_answer(dbase, task_id, answer.GetText(), answer.IsRight())
                if not (answer_id):
                    return False
    return True


# Удаление банка
def delete_bank(dbase, bank_id):
    all_kits_id = []
    all_tests_id = []
    all_tasks_id = []
    all_answers_id = []

    kits = dbase.get_kits_by_bank_id(bank_id)
    if not(kits):
        return False
    # Получаем наборы для удаления
    for kit_id, kit_name in kits:
        all_kits_id.append(kit_id)
        tests = dbase.get_tests_by_kit_id(kit_id)
        if not(tests):
            return False
        # Получаем тесты для удаления
        for test_id, tests_name in tests:
            all_tests_id.append(test_id)
            tasks = dbase.get_tasks_by_test_id(test_id)
            if not(tasks):
                return False
            # Получаем задания для удаления
            for task_id, q_texts in tasks:
                all_tasks_id.append(task_id)
                answers = dbase.get_answers_by_task_id(task_id)
                if not(answers):
                    return False
                # Получаем ответы для удаления
                for answer_id, answers_text, is_right in answers:
                    all_answers_id.append(answer_id)

    # Удаляем
    for id in all_answers_id:
        dbase.delete_data_answer(id)
    for id in all_tasks_id:
        dbase.delete_data_task(id)
    for id in all_tests_id:
        dbase.delete_data_test(id)
    for id in all_kits_id:
        dbase.delete_data_kit(id)
    dbase.delete_data_bank(bank_id)
    return True

# Удаление набора
def delete_kit(dbase, kit_id):
    all_tests_id = []

    tests = dbase.get_tests_by_kit_id(kit_id)
    if not(tests):
        return False
    # Получаем тесты для удаления
    for test_id, tests_name in tests:
        all_tests_id.append(test_id)
        
    for id in all_tests_id:
        dbase.delete_data_test(id)
    dbase.delete_data_kit(kit_id)
    return True


# Редактирование имени банка тестов
def edit_bank_name(dbase, bank_id: int, new_bank_name: str):
    is_updated, error = dbase.update_bank_name(bank_id, new_bank_name)
    if not is_updated:
        print(error)
        return False

    # bank.SetName(new_bank_name)
    return True

# Редактирование имени набора
def edit_kit_name(dbase, kit_id: int, new_kit_name: str):
    is_updated, error = dbase.update_kit_name(kit_id, new_kit_name)
    if not is_updated:
        print(error)
        return False

    # kit.SetName(new_kit_name)
    return True

# Редактирование имени теста
def edit_test_name(dbase, test_id: int, new_test_name: str):
    is_updated, error = dbase.update_test_name(test_id, new_test_name)
    if not is_updated:
        print(error)
        return False

    # test.SetName(new_test_name)
    return True

# Редактирование вопроса
def edit_task_question(dbase, task_id: int, new_task_question: str):
    is_updated, error = dbase.update_task_question(task_id, new_task_question)
    if not is_updated:
        print(error)
        return False

    # task.SetQuestion(new_task_question)
    return True

# Редактирование ответа и правильности ответа
def edit_answer(dbase, answer_id: int, new_answer_text: str, new_is_right: bool):
    is_updated, error = dbase.update_answer(answer_id, new_answer_text, new_is_right)
    if not is_updated:
        print(error)
        return False

    # answer.SetAnswerText(new_answer_text)
    # answer.SetIsRight(new_is_right)
    return True

# Удаление пользователя
def delete_user(dbase, user_id: int):
    is_deleted, error = dbase.delete_data_user(user_id)
    if not is_deleted:
        print(error)
        return False

    return True

# Удаление банка
def delete_bank(dbase, bank_id: int):
    is_deleted, error = dbase.delete_data_bank(bank_id)
    if not is_deleted:
        print(error)
        return False

    return True

# Удаление набора
def delete_kit(dbase, kit_id: int):
    is_deleted, error = dbase.delete_data_kit(kit_id)
    if not is_deleted:
        print(error)
        return False

    return True

# Удаление теста
def delete_test(dbase, test_id: int):
    is_deleted, error = dbase.delete_data_test(test_id)
    if not is_deleted:
        print(error)
        return False

    return True

# Удаление задания
def delete_task(dbase, task_id: int):
    is_deleted, error = dbase.delete_data_task(task_id)
    if not is_deleted:
        print(error)
        return False

    return True

# Удаление ответа
def delete_answer(dbase, answer_id: int):
    is_deleted, error = dbase.delete_data_answer(answer_id)
    if not is_deleted:
        print(error)
        return False

    return True
