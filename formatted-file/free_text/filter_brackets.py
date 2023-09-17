# This is a sample Python script.
import re
import sys
from typing import List, Set, Union


class TextChunk:
    def __init__(self, text: str):
        self.text: str = text
        self.markers: Set[str] = set()

    def add_marker(self, marker: str) -> None:
        self.markers.add(marker)

    def get_text(self, markers_for_filtering: Set[str]) -> Union[str, None]:
        """
        :param markers_for_filtering: list of markers, that should be checked
        :return: text or nothing
        """
        if (
            len(self.markers)
            and markers_for_filtering
            and len(markers_for_filtering) > 0
        ):
            if len(self.markers.intersection(markers_for_filtering)) > 0:
                return self.text
            else:
                return None
        else:
            return self.text


def get_nearest_marker(line: str, markers_in_line: Set[str]) -> Union[str, None]:
    """
    :param line:
    :param markers_in_line:
    :return: nearest marker to the beginning of the line
    """
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
        if nearest_marker != "[]":
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
        markers_in_line: Set[str] = set(get_markers(each_line))
        if len(markers_in_line) > 0:
            chunks: List[TextChunk] = get_chunks_from_line(each_line, markers_in_line)
            chunks_text: List[str] = list()
            for each_chunk in chunks:
                text: str = each_chunk.get_text(white_markers)
                if text is not None:
                    chunks_text.append(text)
            if len(chunks_text) > 0:
                result.append("".join(chunks_text))
        else:
            # no markers in line
            result.append(each_line)
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(" <file template src> <file dest> <marker1> <marker2> <marker3> ... ")
        sys.exit(1)
    file_source: str = sys.argv[1]
    print(f"src: {file_source}")
    file_dest: str = sys.argv[2]
    print(f"dst: {file_dest}")
    markers: Set[str] = set()
    for each_marker in range(3, len(sys.argv)):
        markers.add(sys.argv[each_marker])
    print(markers)
    with open(file_source) as file_src:
        data = file_src.readlines()
    with open(file_dest, "w") as file_dst:
        file_dst.write("\n".join(filter_lines(data, markers)))
