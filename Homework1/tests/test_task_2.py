from src.task_2 import (square,float_addition,float_subtraction,first_five_characters,bool_NAND,bool_XOR)
import pytest
def test_square():

    assert square(5) == 25

    assert square(10) == 100

def test_float_addition():
    #Same Sign
    assert float_addition(0.4, 1.4) == pytest.approx(1.8)
    #Dif sign
    assert float_addition(-0.4, 1.4) == pytest.approx(1.0)

def test_float_subtraction():
    #Same Sign
    assert float_subtraction(2.6, 1.3) == pytest.approx(1.3)
    #Dif Sign
    assert float_subtraction(2.6, -1.3) == pytest.approx(3.9)

def test_first_five_characters():

    assert first_five_characters("Rusty Rebar") == "Rusty"

    assert first_five_characters("One") == "One"

def test_bool_NAND():

    assert bool_NAND(False,False) == True

    assert bool_NAND(False,True) == True

    assert bool_NAND(True,False) == True

    assert bool_NAND(True,True) == False

def test_bool_XOR():

    assert bool_XOR(False,False) == False

    assert bool_XOR(False,True) == True

    assert bool_XOR(True,False) == True

    assert bool_XOR(True,True) == False