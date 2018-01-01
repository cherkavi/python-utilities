#!/usr/bin/python -tt
class Wrapper(object):

    def __init__(self, **kwargs):
        print("__init__", kwargs)
        self.path = kwargs['path']
        self.method = kwargs['method']

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


function_one("this is new message")