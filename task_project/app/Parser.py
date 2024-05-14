import re
from TestClasses.Test import Test
from TestClasses.Task import Task
from TestClasses.Answer import Answer
from TestClasses.Kit import Kit

# Обработка одного варианта шаблона Symbols
def ParserForOneVariantSymbols(test_name : str, input_text : str, split_type : str) -> Test:
    test = Test(test_name)
    text_of_tasks = re.split(str(split_type + split_type + '+'), input_text)
    text_of_tasks = list(filter(lambda x: x not in ['', ' '], text_of_tasks))
    for task_text in text_of_tasks:
        splited_task = re.split(split_type, task_text)
        splited_task = list(filter(lambda x: x not in ['', ' '], splited_task))
        answers = []
        for i in range(1, len(splited_task)):
            if re.match('[*#]',splited_task[i]):
                answers.append(Answer(splited_task[i][1:], True))
            else:
                answers.append(Answer(splited_task[i], False))
        test.AddTask(Task(splited_task[0], answers))
    return test

# Шаблон:
# Вариант 1
# <пробел не обязателен>
# Вопрос1
# Ответ1
# *Ответ2
# Ответ3
# <пробел обязателен>
# Вопрос2
# #Ответ1
# Ответ2
# Ответ3
# <пробел не обязателен>
# Вариант 2
# <пробел не обязателен>
# Вопрос1
# *Ответ1
# Ответ2
# Ответ3

# Обработка варинтов шаблона Symbols
def ParserForSymbols(test_name: str,  task_text : str, kit: Kit, split_type : str) -> None:
    task_text = re.split(r'Вариант\s*\d+', task_text)
    task_text = list(filter(lambda x: x not in ['', ' '], task_text))
    if len(task_text) == 1:
        kit.AddTest(ParserForOneVariantSymbols(test_name, task_text[0], split_type))
        return
    for variant in range(len(task_text)):
        kit.AddTest(ParserForOneVariantSymbols(test_name + ' вариант ' + str(variant + 1), task_text[variant], split_type))
    

# Обравотка одного варианта keys
def ParserForOneVariantKeys(test_name : str, input_text : str, keys : dict[int : str], split_type) -> Test:
    test = Test(test_name)
    text_of_tasks = re.split(str(split_type + split_type + '+'), input_text)
    text_of_tasks = list(filter(lambda x: x not in ['', ' '], text_of_tasks))
    for text_of_task in text_of_tasks:
        splited_task = re.split(split_type, text_of_task)
        splited_task = list(filter(lambda x: x not in ['', ' '], splited_task))
        answers = []

        # получаем номер задания
        if splited_task:
            head_of_task = re.match('(\d+\.) (.*)', splited_task[0])
            if head_of_task:
                number_of_task = int(head_of_task.group(1)[:-1])
                text_of_head = head_of_task.group(2)
            else:
                number_of_task = None
                text_of_head = splited_task[0].strip()
            for i in range(1, len(splited_task)):
                match = re.match('^(\w+\)) (.*)', splited_task[i]) # ищем букву ответа
                if not match:
                    answers.append(Answer(splited_task[i], False))
                    continue
                if number_of_task and number_of_task in keys and match.group(1)[:-1] in keys[number_of_task]:
                    answers.append(Answer(match.group(2), True))
                else:
                    answers.append(Answer(match.group(2), False))

        test.AddTask(Task(text_of_head, answers))
    return test

# Обработка ключей шаблона keys
def GetKeys(keys_text : str, split_type) -> list[dict[int : str]]:
    keys_text = re.split(str(split_type + '+'), keys_text)
    for i in range(len(keys_text)):
        if len(keys_text[i]) == 3:
            keys_text = keys_text[i:]
            break
    keys = []
    key_dict = {}
    for i in range(len(keys_text)):
        if 0 < len(keys_text[i].strip()):
            # Обработка стыков
            if 2 < len(keys_text[i].split()):
                data = keys_text[i].split()
                key_dict[int(data[0])] = data[1]
                keys.append(key_dict)
                key_dict = {int(data[2]): data[3]}
            else:
                keys_text[i] = keys_text[i].split()
                task_num = int(keys_text[i][0])
                key_value = keys_text[i][1]
                if task_num not in key_dict:
                    key_dict[task_num] = key_value
                else:
                    keys.append(key_dict)
                    key_dict = {task_num : key_value}

    keys.append(key_dict)
    return keys

# Шаблон:
# Вариант 1
# <пробел не обязателен>
# 1. Вопрос1
# а) Ответ1
# б) Ответ2
# в) Ответ3
# <пробел обязателен>
# 2. Вопрос2
# а) Ответ1
# б) Ответ2
# в) Ответ3
# <пробел не обязателен>
# Вариант 2
# <пробел не обязателен>
# 1. Вопрос1
# а) Ответ1
# б) Ответ2
# в) Ответ3
# <пробел обязателен>
# 2. Вопрос2
# а) Ответ1
# б) Ответ2
# в) Ответ3
# г) Ответ4
# е) Ответ5
# <пробел не обязателен>
# Ключ/ключ/Ключ/Ключи <может быть какой-то текст>
# <пробел не обязателен>
# 1 а (между 1 а пробел обязателен)
# 2 г
# 1 аб
# 2 е

# Обработка вариантов шаблона keys
def ParserForKeys(test_name : str, file_text : str, kit : Kit, split_type) -> None:
    last_occurrence = max(file_text.rfind("Ключ"), file_text.rfind("ключ"))
    task_text = re.split(r'Вариант\s*\d+', file_text[:last_occurrence])
    task_text = list(filter(lambda x: x not in ['', ' '], task_text))

    keys_text = file_text[last_occurrence:]
    keys = GetKeys(keys_text, split_type)
    
    if len(task_text) == 1:
        kit.AddTest(ParserForOneVariantKeys(test_name, task_text[0], keys[0], split_type))
        return

    for variant in range(len(task_text)):
        kit.AddTest(ParserForOneVariantKeys(test_name + ' вариант ' + str(variant + 1), task_text[variant], keys[variant], split_type))


# Обрботка одного врианта AnswerUnderQuestion
def ParserForOneVariantAnswerUnderQuestion(test_name : str, input_text : str, split_type) -> Test:
    test = Test(test_name)
    text_of_tasks = re.split(str(split_type + split_type + '+'), input_text)
    text_of_tasks = list(filter(lambda x: x not in ['', ' '], text_of_tasks))
    for task_text in text_of_tasks:
        splited_task = re.split(split_type, task_text)
        splited_task = list(filter(lambda x: x not in ['', ' '], splited_task))

        # Получаем ответы
        task_answers = []
        for text in splited_task[-1].split():
            if text.isdigit():
                task_answers.append(text)


        answers = []
        for i in range(1, len(splited_task) - 1):
            text_of_answer = splited_task[i].strip()

            # Получаем номер задания
            num = ''
            for u in range(0, len(text_of_answer)):
                if text_of_answer[u].isdigit():
                    num += text_of_answer[u]
                else:
                    for y in range(u, len(text_of_answer)):
                        if text_of_answer[y].isalnum() or text_of_answer[y].isdigit():
                            answer_text = text_of_answer[y:]
                            break
                    break
            if num in task_answers:
                answers.append(Answer(answer_text.strip(), True))
            else:
                answers.append(Answer(answer_text.strip(), False))
        test.AddTask(Task(splited_task[0], answers))
    return test

# Шаблон:
# Вариант 1
# <пробел не обязателен>
# Вопрос1
# 1. Ответ1
# 2. Ответ2
# 3. Ответ3
# Ответ: 2
# <пробел обязателен>
# Вопрос2
# 1. Ответ1
# 2. Ответ2
# 3. Ответ3
# Ответ: 1
# <пробел не обязателен>
# Вариант 2
# <пробел не обязателен>
# Вопрос1
# 1. Ответ1
# 2. Ответ2
# 3. Ответ3
# Ответ: 1 3

# Обработка вариантов AnswerUnderQuestion
def ParserForAnswerUnderQuestion(test_name: str, task_text : str, kit: Kit, split_type) -> None:
    task_text = re.split(r'Вариант\s*\d+', task_text)
    task_text = list(filter(lambda x: x not in ['', ' '], task_text))
    if len(task_text) == 1:
        kit.AddTest(ParserForOneVariantAnswerUnderQuestion(test_name, task_text[0], split_type))
        return
    for variant in range(len(task_text)):
        kit.AddTest(ParserForOneVariantAnswerUnderQuestion(test_name + ' вариант ' + str(variant + 1), task_text[variant], split_type))


# Принимает имя теста(введено пользователем), текст для обработки,
# набор в который добавятся тесты и input_mode(смотри Constants.py)
def Parse(test_name : str, input_text : str, kit : Kit,  input_type : str, split_type : str) -> bool:
    try:
        match input_type:
            case "symbol":
                ParserForSymbols(test_name, input_text, kit, split_type)
            case "key":
                ParserForKeys(test_name, input_text, kit, split_type)
            case "answer":
                ParserForAnswerUnderQuestion(test_name, input_text, kit, split_type)
    except:
        return False
    return True