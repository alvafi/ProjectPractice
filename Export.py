import xml.etree.ElementTree as ET
from io import BytesIO
import io

def MakeXML(dbase, test_id):
    # Создаем XML-структуру
    root = ET.Element("quiz")
    question_number = 1

    tasks = dbase.get_tasks_by_test_id(test_id)
    if not tasks:
        return False
    
    for task_id, question_text in tasks:
        question = ET.SubElement(root, "question", type="multichoice")
        name = ET.SubElement(question, "name")
        text = ET.SubElement(name, "text")
        text.text = f"Вопрос {question_number}"
        questiontext = ET.SubElement(question, "questiontext", format="html")
        questiontext.text = question_text
        answer_number = 1

        answers = dbase.get_answers_by_task_id(task_id)
        if not answers:
            return False
        
        for answer_id, text_of_answer, is_right in answers:
            answer_element = ET.SubElement(question, "answer", fraction="1" if is_right else "0")
            answer_text = ET.SubElement(answer_element, "text")
            answer_text.text = text_of_answer
            answer_number += 1

        question_number += 1

    # Создаем XML-файл
    tree = ET.ElementTree(root)
    xml_data = io.BytesIO()
    tree.write(xml_data)

    xml_data.seek(0)
    return xml_data


def MakeQti(dbase, test_id):
    test_name = dbase.get_test_name_by_test_id(test_id)
    if not test_name:
        return False

    root = ET.Element("assessment", title=test_name)

    tasks = dbase.get_tasks_by_test_id(test_id)
    if not tasks:
        return False
    
    for task_id, question_text in tasks:
        item = ET.SubElement(root, "item", title=question_text)
        
        answers = dbase.get_answers_by_task_id(task_id)
        if not answers:
            return False
        
        for answer_id, text_of_answer, is_right in answers:
            if is_right:
                correct_response = ET.SubElement(item, "correct_response")
                value = ET.SubElement(correct_response, "value")
                value.text = text_of_answer
            simple_choice = ET.SubElement(item, "simpleChoice", identifier=text_of_answer)
            simple_choice.text = text_of_answer

    tree = ET.ElementTree(root)
    xml_data = io.BytesIO()
    tree.write(xml_data, encoding='utf-8', xml_declaration=True)
    
    xml_data.seek(0)
    return xml_data

def Export(dbase, test_id, export_mode):
    match export_mode:
        case "xml":
            return MakeXML(dbase, test_id)
        case "qti":
            return MakeQti(dbase, test_id)
        
