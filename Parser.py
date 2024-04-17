import re
import Test
import Task
import Answer

def ParserForTxt(input_text : str, test : Test) -> None:
    text_of_tasks = re.split('\n\n+', input_text)
    text_of_tasks = list(filter(lambda x: x != '', text_of_tasks))
    
    for task_text in text_of_tasks:
        splited_task = re.split('\n', task_text)

        answers = []
        for i in range(1, len(splited_task)):
            if re.match('[*#]',splited_task[i]):
                answers.append(Answer.Answer(splited_task[i][1:], True))
            else:
                answers.append(Answer.Answer(splited_task[i], False))
        test.AddTask(Task.Task(splited_task[0], answers))



def ParserWithLetersAndKeys(input_text : str, keys : list[tuple[int, str]], test : Test) -> None:
    text_of_tasks = re.split('\n\n+', input_text)
    text_of_tasks = list(filter(lambda x: x != '', text_of_tasks))
    
    for task_text in text_of_tasks:
        #splited_task = re.split('\s*+[а-яё]+\)+\s*(?=\w)', task_text)
        splited_task = re.split('\n', task_text)
        answers = []
        for i in range(1, len(splited_task)):
            if re.match('[*#]',splited_task[i]):
                answers.append(Answer.Answer(splited_task[i][1:], True))
            else:
                answers.append(Answer.Answer(splited_task[i], False))
        test.AddTask(Task.Task(splited_task[0], answers))
