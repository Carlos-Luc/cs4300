from src.task_2 import (square,float_addition,float_subtraction,first_five_characters,bool_NAND,bool_XOR)
import pytest

#Squaring both positive and negative
@pytest.mark.parametrize("number,expected",[(5,25),(-10,100)])

def test_square(number,expected):

    assert square(number) == expected

#Same sign then differnt sign
@pytest.mark.parametrize("first,second,expected", [(0.4,1.4,1.8),(-0.4,1.4,1.0)])

def test_float_addition(first,second,expected):

    assert float_addition(first, second) == pytest.approx(expected)

#Same sign then diffrent sign
@pytest.mark.parametrize("first,second,expected", [(2.6,1.3,1.3),(2.6,-1.3,3.9)])

def test_float_subtraction(first,second,expected):
    
    assert float_subtraction(first, second) == pytest.approx(expected)

#Testing more than 5 characters and less than 5
@pytest.mark.parametrize("string,expected", [("Rusty Rebar","Rusty"),("One","One")])

def test_first_five_characters(string,expected):

    assert first_five_characters(string) == expected
#Truth table of NAND
@pytest.mark.parametrize("first,second,expected", [(False,False,True),(False,True,True),(True,False,True),(True,True,False)])

def test_bool_NAND(first,second,expected):

    #Using 'is' to prevent truthy or falsy values to pass test, only bool result is expected
    assert bool_NAND(first,second) is expected

@pytest.mark.parametrize("first,second,expected", [(False,False,False),(False,True,True),(True,False,True),(True,True,False)])

def test_bool_XOR(first,second,expected):

    assert bool_XOR(first,second) is expected