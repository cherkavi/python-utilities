# ----------------------------------------
# function without parameters
def my_simple_decorator(function):
    def simple_decorator():
        return_value=function()        
        print(f"simple wrapper: {return_value}")
        return return_value
    return simple_decorator

@my_simple_decorator
def summarize2()->int:
    return 10


# ----------------------------------------
# with function parameters
def my_decorator(target_function):
    def decorator(*args, **kwargs):
        return_value=target_function(*args, **kwargs)        
        print(f"wrapper: {return_value}")
        return return_value
    return decorator

@my_decorator
def summarize(a:int, b:int)->int:
    return a+b

# ----------------------------------------
# function without parameters, decorator with parameters 
def my_another_decorator(*args, **kwargs):
    def another_decorator(func):
        print(kwargs['description'])
        return func
    return another_decorator

@my_another_decorator(description="another description: ")
def summarize_another()->int:
    return 20

# ----------------------------------------
# function with parameters, decorator with parameters 
def my_complex_decorator(description:str):
    def complex_decorator(func):
        def complex_decorator_wrapper(*args, **kwargs):
            return_value = func(*args, **kwargs)
            print(f"{description}:  {return_value}")
            return return_value
        return complex_decorator_wrapper
    return complex_decorator

@my_complex_decorator(description="my own description: ")
def summarize_complex(a:int)->int:
    return a+a


if __name__=='__main__':
    print(f"main.summarize2: {summarize2()}")
    print("------------")
    print(f"main.summarize: {summarize(30,40)}")
    print("------------")
    print(f"main.summarize: {summarize_another()}")
    print("------------")
    print(f"main.summarize_complex: {summarize_complex(20)}")