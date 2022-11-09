# test

## doctest

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/test/doctest.py) -->
<!-- The below code snippet is automatically added from ../../python/test/doctest.py -->
```py
def summarize_digits(a:int, b:int) -> int:
    """
    example of using doctest
    to execute it: 
        python3 -m doctest -v implementation.py
    or you can execute prepared text file:
        python3 -m doctest -v implementation.txt
    >>> summarize_digits(10,5)
    15
    """
    return a+b
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## pytest

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/test/pytest.py) -->
<!-- The below code snippet is automatically added from ../../python/test/pytest.py -->
```py
import pytest
from implementation import summarize_digits

# for execution just run
# pytest .
@pytest.fixture(scope='function')
def some_resource(request):
    stuff_i_setup = ["I setup"]

    def some_teardown():
        stuff_i_setup[0] += " ... but now I'm torn down..."
        print(stuff_i_setup[0])
    request.addfinalizer(some_teardown)

    return stuff_i_setup[0]

@pytest.yield_fixture(scope="function")
def var_a():
    yield 5

@pytest.yield_fixture(scope="function")
def var_b():
    yield 10

def test_one(var_a, var_b):
    # given
    a=5
    b=10
    # when 
    result = summarize_digits(var_a, var_b)
    # then 
    assert result == 15
```
<!-- MARKDOWN-AUTO-DOCS:END -->


