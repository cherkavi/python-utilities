#!/usr/bin/env python3
import os
import shutil
import sys
from typing import List


# list to parts, split list
# split text file to bunch of parts:
# - { text file } { amount of expected parts }
# - { text file } { start line :included } { end line :included }

def count_amount_of_lines(path_to_file):
    with open(path_to_file) as text_file:
        line_counter = 0
        for each_line in text_file:
            if each_line and len(each_line.strip()) > 0:
                line_counter = line_counter + 1
    return line_counter


def check_output_folder(output_folder: str = "parts") -> str:
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)
    return output_folder


class NamingStrategy:
    def get_part(self, part_number: int) -> str:
        pass


class FixName(NamingStrategy):
    def __init__(self, root_folder: str):
        self.root_folder = root_folder

    def get_part(self, part_number: int) -> str:
        return (self.root_folder + "/part_%s") % (part_number,)


class PredefinedNames(NamingStrategy):

    def __init__(self, root_folder: str, path_to_file: str):
        self.root_folder = root_folder
        self.names: List[str] = list()
        with open(path_to_file, "r") as file_with_names:
            self.names = [each_line.strip() for each_line in file_with_names if len(each_line.strip()) > 0]

    def get_part(self, part_number: int) -> str:
        return self.root_folder + "/" + (
            self.names[part_number] if part_number < len(self.names) else self.names[part_number % len(self.names)])

    @property
    def count(self) -> int:
        return len(self.names)


def split_file_to_parts(path_to_file: str, parts: int, part_naming: NamingStrategy):
    amount_of_lines = count_amount_of_lines(path_to_file)
    part_size = int(amount_of_lines / parts)
    part_size = part_size if part_size > 1 else part_size + 1

    output_file = None
    with open(path_to_file) as text_file:
        line_counter = 0
        for each_line in text_file:
            line_counter = line_counter + 1
            if line_counter % part_size == 1:
                if output_file:
                    output_file.close()
                output_file = open(part_naming.get_part(int(line_counter / part_size)), "w")
            print(each_line, file=output_file, end='')
    output_file.close()


def is_int(value) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("1. expected input parameters: <filename> <output folder> <amount of parts>")
        print("2. expected input parameters: <filename> <output folder> <path to file with names>")
        sys.exit(1)
    filename = sys.argv[1]
    output_folder = sys.argv[2]
    if is_int(sys.argv[3]):
        amount_of_parts = int(sys.argv[3])
        split_file_to_parts(filename, amount_of_parts, FixName(output_folder))
    else:
        path_to_file_with_names = sys.argv[3]
        naming_strategy: PredefinedNames = PredefinedNames(output_folder, path_to_file_with_names)
        split_file_to_parts(filename, naming_strategy.count, naming_strategy)
