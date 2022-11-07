## select arguments from separated comma list
## usage
# python3 input-argument-selector.py prod,staging user1,user2,user3

import os
import sys
from typing import List

def read_input():
    # from getkey import getkey, keys
    return input()

def print_values(values: List[str]):
    counter = 0;
    for each_value in values:
        counter+=1
        print(f"{counter:<3}  {each_value}")

def get_one_parameter(comma_separated_values:str) -> str:
    values:List[str] = comma_separated_values.split(",")
    while True:
        print_values(values)
        choice = read_input()
        if not choice.strip().isnumeric():
            print("not a number, try again")
            continue
        choice_number: int = int(choice.strip())
        if not 1<=choice_number<=len(values):
            print("select value in range ")
            continue
        return values[choice_number-1]


if __name__=="__main__":
    result_arguments:List[str]=list()
    for each_param in sys.argv[1:]:
        result_arguments.append(get_one_parameter(each_param))   
    print(" ".join(result_arguments))
