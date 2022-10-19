class Foo:
    def bar1(self):
        print(1)
    def bar2(self):
        print(2)

def call_method(o, name):
    return getattr(o, name)()


f = Foo()
