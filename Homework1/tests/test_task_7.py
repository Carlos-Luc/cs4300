from src.task_7 import dot_product
import numpy as np

def test_dot_product_1D():

    first = np.array([2,3])

    second = np.array([4,5])

    assert dot_product(first,second) == 23

def test_dot_product_2D():

    first = np.array([[1,2],[3,4]])

    second = np.array([[5,6],[7,8]])

    result = dot_product(first,second)

    assert result.tolist() == [[19,22],[43,50]]
