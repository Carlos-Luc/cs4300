from src.task_3 import(sign_check,sum_one_to_hundered,first_ten_primes)
import pytest

@pytest.mark.parametrize("number,expected",[(10,"positive"),(1.5,"positive"),(0,"zero"),(0.0,"zero"),(-5,"negative"),(-5.3,"negative")])

def test_sign_check(number,expected):

    assert sign_check(number) == expected

def test_first_ten_primes(capsys):

    first_ten_primes()

    captured = capsys.readouterr()

    assert captured.out == "2\n3\n5\n7\n11\n13\n17\n19\n23\n29\n" 

def test_sum_one_to_hundered():

    assert sum_one_to_hundered() == 5050