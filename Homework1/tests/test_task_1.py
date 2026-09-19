from src.task_1 import hello_world

def test_hello_world(capsys):
    
    hello_world()

    captured = capsys.readouterr()

    assert captured.out.strip() == "Hello World!"