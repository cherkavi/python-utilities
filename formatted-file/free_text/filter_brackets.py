# Parse each line of free text
# find out all tags like [aaAA] and remain or remove part of the line from the left of it
# ( till the beginning or next tag )
# Special tags:
# [last_comma] - remove last comma in the line, when it exists
import re
import sys
from typing import List, Set, Union

# list of special tag for changing way of processing
SPECIAL_MARKER_LAST_COMMA: str = "[last_comma]"
""" remove last comma ( from the end of the line ) if it exists, line will be right-trimmed """
SPECIAL_MARKER_PREFIX: str = "[prefix]"
""" marker that remains in the line only when exist at least one another """
SPECIAL_MARKER_ALWAYS: str = "[]"
""" text with this marker will be added without any conditions, always present """

SPECIAL_MARKER_CONTROL_PREFIX: str = "[control_"
""" if           no marker in the line starts with this prefix                                   - normal flow  
    if at least one marker in the line starts with this prefix and     present in the white-list - normal flow
    if at least one marker in the line starts with this prefix and not present in the white-list - remove the line """

SPECIAL_MARKERS_POSTPROCESSING: List[str] = [
    SPECIAL_MARKER_LAST_COMMA,
]


class TextChunk:
    def __init__(self, text: str):
        self.text: str = text
        self.markers: Set[str] = set()
        """ list of markers like '[ab]' '[bc]' """

    def __repr__(self):
        return f"{self.text}: {self.markers}"

    def add_marker(self, marker: str) -> None:
        self.markers.add(marker)

    def is_prefix(self) -> bool:
        return SPECIAL_MARKER_PREFIX in self.markers

    def get_text(self, markers_for_filtering: Set[str]) -> Union[str, None]:
        """
        :param markers_for_filtering: list of markers, that should be checked
        :return: text (passed) or nothing ( not passed )
        """
        if len(self.markers) == 0:
            return self.text
        if SPECIAL_MARKER_ALWAYS in self.markers:
            return self.text
        if SPECIAL_MARKER_PREFIX in self.markers:
            return self.text
        if markers_for_filtering is None or len(markers_for_filtering) == 0:
            return self.text
        if len(self.markers.intersection(markers_for_filtering)) > 0:
            return self.text
        else:
            return None


def remove_special_markers_from_collection(list_of_markers: Set[str]) -> Set[str]:
    result: Set[str] = set(list_of_markers)
    for each_special_marker in SPECIAL_MARKERS_POSTPROCESSING:
        if each_special_marker in result:
            result.remove(each_special_marker)
    return result


def remove_special_markers_from_line(line: str) -> str:
    result: str = line
    for each_special_marker in SPECIAL_MARKERS_POSTPROCESSING:
        result = result.replace(each_special_marker, "")
    return result


def get_nearest_marker(line: str, markers_in_line: Set[str]) -> Union[str, None]:
    """
    :param line:
    :param markers_in_line:
    :return: nearest marker to the beginning of the line
    """
    markers: Set[str] = set(markers_in_line)
    minimal_index: int = len(line)
    result: str = None
    for each_marker in markers_in_line:
        next_index: int = line.find(each_marker)
        if next_index < 0:
            continue
        if next_index < minimal_index:
            result = each_marker
            minimal_index = next_index
    if minimal_index == len(line):
        return None
    else:
        return result


def get_chunks_from_line(line: str, markers_in_line: Set[str]) -> List[TextChunk]:
    current_line: str = line
    result: List[TextChunk] = list()
    while len(current_line) > 0:
        nearest_marker: str = get_nearest_marker(current_line, markers_in_line)
        if nearest_marker is None:
            # no markers in the line left
            result.append(TextChunk(current_line))
            break
        nearest_marker_position = current_line.index(nearest_marker)
        if nearest_marker_position == 0:
            if len(result) > 0:
                result[len(result) - 1].add_marker(nearest_marker)
            else:
                next_chunk = TextChunk("")
                next_chunk.add_marker(nearest_marker)
                result.append(next_chunk)
            current_line = current_line[len(nearest_marker) :]
            continue
        next_chunk = TextChunk(current_line[:nearest_marker_position])
        if nearest_marker != SPECIAL_MARKER_ALWAYS:
            # avoid to have empty marker in the set
            next_chunk.add_marker(nearest_marker)
        result.append(next_chunk)
        current_line = current_line[nearest_marker_position + len(nearest_marker) :]
    return result


def get_markers(input_string: str) -> Set[str]:
    """
    :param input_string: string for searching for markers like [ab] [abdsa01] ...
    :return: markers like "[ab]" in the set
    """
    pattern = r"\[([^]]*)\]"
    # pattern = r'\[[^\]]+\](?=(?:\s*\.?$)|\s*$)'
    markers: List[str] = re.findall(pattern, input_string)
    return set([f"[{each_marker}]" for each_marker in markers])


def get_all_markers(chunks: List[TextChunk]) -> Set[str]:
    result: Set = set()
    for each_chunk in chunks:
        result.update(each_chunk.markers)
    return result


def has_control_marker(markers: Set[str]) -> bool:
    for each_marker in markers:
        if each_marker.startswith(SPECIAL_MARKER_CONTROL_PREFIX):
            return True
    return False


def is_control_marker_in_white_list(markers: Set[str], white_markers: Set[str]) -> bool:
    control_markers: Set[str] = set()
    for each_marker in markers:
        if each_marker.startswith(SPECIAL_MARKER_CONTROL_PREFIX):
            control_markers.add(each_marker)
    return len(white_markers.intersection(control_markers)) > 0


def filter_lines(lines: List[str], white_markers: Set[str]) -> List[str]:
    """
    this
    :param lines: lines with text for analyzing
    :param white_markers: list of the markers that should be present in output text
    :return:
    """
    result: List[str] = []
    for each_line in lines:
        each_line = each_line.rstrip(" ")
        each_line = each_line.rstrip("\n")
        markers_in_line: Set[str] = set(get_markers(each_line))
        each_line = remove_special_markers_from_line(each_line)
        if len(markers_in_line) == 0:
            # no markers in line
            result.append(each_line)
            continue

        chunks: List[TextChunk] = get_chunks_from_line(
            each_line, remove_special_markers_from_collection(markers_in_line)
        )

        chunks_text: List[str] = list()
        chunk_counter_prefix: int = 0
        chunk_counter_added: int = 0
        for each_chunk in chunks:
            text: str = each_chunk.get_text(white_markers)
            if text is not None and len(text.strip()) > 0:
                chunks_text.append(text)
                chunk_counter_added += 1
                if each_chunk.is_prefix():
                    chunk_counter_prefix += 1
        if chunk_counter_prefix == chunk_counter_added:
            continue  # next line, current line has no "white labeled chunks" only "additional/prefixes"

        if len(chunks_text) == 0:
            continue  # next line

        filtered_string = "".join(chunks_text)

        if SPECIAL_MARKER_LAST_COMMA in markers_in_line:
            new_line_candidate: str = filtered_string.rstrip()
            if new_line_candidate.endswith(","):
                filtered_string = new_line_candidate[0: len(new_line_candidate) - 1]

        all_markers_in_line: Set[str] = get_all_markers(chunks)
        if has_control_marker(all_markers_in_line):
            if is_control_marker_in_white_list(all_markers_in_line, white_markers):
                result.append(filtered_string)
            else:
                pass
        else:
            result.append(filtered_string)

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(" <file template src> <file dest> <marker1> <marker2> <marker3> ... ")
        sys.exit(1)
    if len(sys.argv) == 2:
        # print all markers logic
        with open(sys.argv[1], "r") as file_src:
            markers_all: Set[str] = set()
            for each_line in file_src.readlines():
                markers_all.update(get_markers(each_line))
        markers_all.remove(SPECIAL_MARKER_ALWAYS)
        output_list: List[str] = list(markers_all)
        output_list.sort()
        [print(element) for element in output_list]
        sys.exit(0)
    file_source: str = sys.argv[1]
    print(f"src: {file_source}")
    file_dest: str = sys.argv[2]
    print(f"dst: {file_dest}")
    markers: Set[str] = set()
    for each_marker in range(3, len(sys.argv)):
        markers.add(sys.argv[each_marker])
    print(markers)
    with open(file_source, "r") as file_src:
        data = file_src.readlines()
    with open(file_dest, "w") as file_dst:
        file_dst.write("\n".join(filter_lines(data, markers)))
