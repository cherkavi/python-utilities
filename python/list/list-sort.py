my_list = [5,4,2,1]

def get_sort_reverse_function(max_element: int):
    def sort_reverse_function(element) -> int:
        return max_element-element
    return sort_reverse_function

def sort_function(element) -> int:
    return element

my_list.sort(key=get_sort_reverse_function(max(my_list)))
print("reverse sort:"+ str(my_list))

my_list.sort(key=sort_function)
print("sort: "+ str(my_list))
