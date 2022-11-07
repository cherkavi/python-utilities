def set_varibale_by_name(source:dict, name_of_variable_to_set:str, value):
    """ set variable by name, dynamically set variable
    """
    source[name_of_variable_to_set] = value
    # globals()[name_of_variable_to_set] = value

if __name__=="__main__":
    set_varibale_by_name(locals(), "a", 10)
    set_varibale_by_name(locals(), "b", "hello")

    print(a)
    print(b)
