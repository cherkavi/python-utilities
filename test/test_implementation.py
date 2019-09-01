from implementation import summarize_digits
# for execution just run
# pytest .

def setup():
    print("setup")

def test_one():
    # given
    a=5
    b=10
    # when 
    result = summarize_digits(a,b)
    # then 
    assert result == 15