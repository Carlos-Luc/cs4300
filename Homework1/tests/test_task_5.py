from src.task_5 import list_slice, create_student_dict

def test_list_slice(capsys):

    list_slice()

    captured = capsys.readouterr()

    assert captured.out =="('Grapes of Wrath', 'John Steinbeck')\n('Red Rising', 'Pierce Brown')\n('The Count of Monte Cristo', 'Alexander Dumas')\n"

def test_create_student_dict():

    database = create_student_dict()

    assert database["Alice"] == 1

    assert database["Bob"] == 2

    assert database["Eve"] == 3

