import pytest
from packaging_example.my_module import fib

test_data = [
    (0, 0),
    (1, 1),
    (2, 1),
    (3, 2),
    (4, 3),
    (5, 5),
    (6, 8),
    (7, 13),
    (8, 21),
    (9, 34),
    (10, 55),
    (11, 89),
    (12, 144),
    (13, 233),
    (14, 377),
]


@pytest.mark.parametrize("i,expected", test_data)
def test_fib(i, expected):
    assert fib(i) == expected
