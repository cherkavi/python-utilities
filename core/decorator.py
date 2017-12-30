#!/usr/bin/python -tt
class Wrapper(object):
    Reestr = list()

    def __init__(self, external_function):
        self.func = external_function
        Wrapper.Reestr.append(external_function) 

    def __call__(self):
        print ">>> call:", self.func.__name__, " of ", [x.__name__ for x in Wrapper.Reestr]
        self.func()
        print "<<< call", self.func.__name__

@Wrapper
def function_one():
    print "output function_one"

@Wrapper
def function_two():
    print "output function_two"

function_one()
function_two()