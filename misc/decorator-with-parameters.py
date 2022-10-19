#!/usr/bin/python -tt
class Wrapper(object):
    LIST_OF_WRAPPERS = list()

    def __init__(self, **kwargs):
        print("__init__", self, kwargs)
        self.path = kwargs['path']
        self.method = kwargs['method']
        Wrapper.LIST_OF_WRAPPERS.append(self)

    def __call__(self, external_function, *args, **kwargs):
    	print("__call__", external_function)

    	def real_decorator(*args, **kwargs):
    		new_value = ",".join([self.path, self.method, args[0]])
    		new_arguments_tuple = (new_value, )
    		return external_function(*new_arguments_tuple, **kwargs)

    	return real_decorator


@Wrapper(path="my new path", method="force")
def function_one(message):
    print("output function_one: " + message)


@Wrapper(path="my another path", method="peaceful")
def function_two(message):
    print("output function_two: " + message)

function_one("this is new message")
function_two("this is new message")