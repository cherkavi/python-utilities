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
def test_one():
    # given
    a=5
    b=10
    # when 
    result = summarize_digits(a,b)
    # then 
    assert result == 15