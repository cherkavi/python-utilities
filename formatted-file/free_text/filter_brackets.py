# This is a sample Python script.
import re
from typing import List, Set


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def get_markers(input_string: str) -> List[str]:
    pattern = r'\[([^]]+)\]'
    # pattern = r'\[[^\]]+\](?=(?:\s*\.?$)|\s*$)'
    return re.findall(pattern, input_string)


def remove_markers(line: str, markers: Set[str]) -> str:
    # Define a regular expression pattern to match [ab] and [bc]
    result: str = line
    for each_marker in markers:
        escaped_pattern = re.escape(f"[{each_marker}]")
        result = re.sub(re.compile(escaped_pattern), '', result)
    return result


def filter_lines(lines: List[str], white_markers: Set[str]) -> List[str]:
    """
    this
    :param lines: lines with text for analyzing
    :param white_markers: list of the markers that should be present in output text
    :return:
    """
    result: List[str] = []
    for each_line in lines:
        each_line = each_line.strip("\n")
        if len(get_markers(each_line)):
            parts: List[str] = each_line.split(".")
            parts_result: List[str] = []
            for each_part in parts:
                if each_part == "\n":
                    continue
                if len(each_part) == 0:
                    continue
                markers: Set[str] = set(get_markers(each_part))
                if len(markers) > 0:
                    # string has markers
                    if len(markers.intersection(white_markers)) > 0:
                        parts_result.append(remove_markers(each_part, markers))
                    else:
                        pass
                else:
                    # no markers in the part of the string
                    parts_result.append(each_part)
            if len(parts_result) > 0:
                result.append(".".join(parts_result) + ".")
        else:
            # no markers in line
            result.append(each_line)
    return result
