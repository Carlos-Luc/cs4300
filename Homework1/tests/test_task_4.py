from src.task_4 import calculate_discount
import pytest
#Handles valid inputs such as int and float prices and discounts, 0% discount and 100% discount 
@pytest.mark.parametrize("price,discount,final",[(100,15,85.00),(100.25,15,85.21),(100,12.9,87.10),(100.25,12.9,87.32),(100,0,100.00),(100,100,0)])

def test_valid_calculate_discount(price,discount,final):

    assert calculate_discount(price, discount) == pytest.approx(final)

#Handles invalid inputs such as negative prices,discounts under zero and over 100 and nonnumeric discounts and prices
@pytest.mark.parametrize("price,discount,expected_exception",[(-100,15,ValueError),(100,-15,ValueError),(100,101,ValueError),("100",15,TypeError),(100,"15",TypeError)])

def test_invald_calculate_discount(price,discount,expected_exception):

    with pytest.raises(expected_exception):

        assert calculate_discount(price,discount)
