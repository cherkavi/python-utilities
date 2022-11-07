# example of overriding operators
# operator overriding
class Value:
    def __init__(self, value):
        self.value = value

    # - __sub__, * __mul__, ** __pow__, / __truediv__, // __floordiv__, % __mod__
    # << __lshift__, >> __rshift__, & __and__, | __or__, ^ __xor__, ~ __invert__
    # < __lt__, <= __le__, == __eq__, != __ne__, > __gt__, >= __ge__
    def __add__(self, other):
        return Value(" -[ "+self.value +" ]-  -[ "+ other.value+" ]- ")

    def __str__(self):
        return self.value


v1 = Value("line#1")
v2 = Value("line#2")
print(v1 + v2)
