def print_arguments_as_list(*input_arguments_as_list):
    for each_argument in input_arguments_as_list:
        print(each_argument)

print("----")
print_arguments_as_list("this", "is", "multipy", "arguments")


def print_arguments_as_map(**input_arguments_as_map):
    for each_argument in input_arguments_as_map:
        print(each_argument, input_arguments_as_map[each_argument])

print("----")
print_arguments_as_map(arg_1 = "this", arg_2 = "is", arg_3 = "multipy", arg_4 = "arguments")


def print_arguments_as_map(*input_arguments_as_list, **input_arguments_as_map):
    for each_argument in input_arguments_as_list:
        print(each_argument)
    for each_argument in input_arguments_as_map:
        print(each_argument, input_arguments_as_map[each_argument])

print("----")
print_arguments_as_map("this", "is", "multipy", "arguments", arg_1 = "this", arg_2 = "is", arg_3 = "multipy", arg_4 = "arguments")


# example of assignment of many elements
first_element, *rest_of_elements = [1,2,3,4,5]
print(first_element, rest_of_elements)
