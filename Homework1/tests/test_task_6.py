from src.task_6 import text_file_word_count
import pytest

def test_text_file_word_count():

   assert text_file_word_count("task_6_read_me.txt") == 127


@pytest.mark.parametrize("content, expected_word_count",[("",0),("Hello World",2),("one two\n three",3),("Space       Test",2)])

def test_text_file_word_count_parameters(tmp_path,content,expected_word_count):

   file_path = tmp_path / "sample.txt"

   file_path.write_text(content)

   assert text_file_word_count(file_path) == expected_word_count