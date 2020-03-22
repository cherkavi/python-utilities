def my_custom_wrapper(target_function, *args, **kwargs):
    def my_wrapper(*args, **kwargs):
        print("arguments: " + str(args))
        return_value = target_function(*args, **kwargs)
        print("return value: "+str(return_value))
        return return_value
    return my_wrapper

@my_custom_wrapper
def sum(a=10, b=None):
    if not b:
        b = a
    return a+b


if __name__=='__main__':
    print(sum(10,20))