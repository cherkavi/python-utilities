import sys
import re

def check_function(s, pattern=re.compile(r"[\w/]+:[\w/]+")):
    # regular expression function
    if not pattern.match(s):
        raise TypeError()
    return s

class ArgumentParser:
    """
    simple parser for sys.argv - just allow access by index with "checking type"
    """
    def __init__(self, checking_functions=None):
        self.arguments = sys.argv
        self.checking_functions = checking_functions

    def __getitem__(self, index):
        item = index+1
        if item > len(self.arguments):
            return None
        else:
            if item in self.checking_functions:
                return self.checking_functions[item](self.arguments[item])
            else:
                return self.arguments[item]

if __name__ == '__main__':
    input_arg_parser = ArgumentParser({1: check_function})
    create_image(input_arg_parser[0], input_arg_parser[1], input_arg_parser[2])
