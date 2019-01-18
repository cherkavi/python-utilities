import sys
import re


def remove_prefix(prefix, value):
    # remove prefix from value if prefix found
    if value.startswith(prefix):
        return value[len(prefix):]
    else:
        return value


def first_alphabet_char_position(value):
    """ find first position of [a-zA-Z] character into string """
    match = re.search("[a-zA-Z]", value)
    if match:
        return match.start()
    else:
        return -1


def set_new_element_to_path(list_with_elements, current_position, previous_position, element):
    while len(list_with_elements) < current_position + 1:
        list_with_elements.append("")

    if current_position < previous_position:
        list_with_elements = list_with_elements[0:current_position + 1]

    list_with_elements[current_position] = element
    return list_with_elements


class Component:
    def __init__(self, raw_string):
        elements = raw_string.split(":")
        self.name = elements[1]
        self.version = elements[3] if len(elements[3]) > 0 else None

    @classmethod
    def init_string(cls, name, version):
        return "xxx:%s:xxx:%s" % (name, version)

    def __str__(self):
        return "%s:%s" % (self.name, self.version)

    def __eq__(self, other):
        if not isinstance(other, Component):
            return False
        if other.version and self.version:
            return other.name == self.name and other.version == self.version
        else:
            return other.name == self.name


if __name__ == "__main__":
    """ after execution command 'mvn dependency:tree '"""
    search_component_name = sys.argv[1]
    search_component_version = "" if len(sys.argv) <= 2 else sys.argv[2]
    search_component = Component(Component.init_string(search_component_name, search_component_version))

    last_rank = 0
    path = list()
    for each_line in sys.stdin:
        line = remove_prefix("[INFO] ", each_line).strip()
        if len(line) == 0:
            continue
        rank = int(first_alphabet_char_position(line) / 3)
        component = Component(line)
        path = set_new_element_to_path(path, rank, last_rank, component)
        last_rank = rank
        if component == search_component:
            print(" <- ".join(
                [str(path[index]) if (index + 1) == len(path) else path[index].name for index in range(len(path))]))
