# pip install ruamel.yaml
#
from copy import deepcopy
from typing import List, Union, Set
import ruamel.yaml
from ruamel.yaml.comments import CommentedMap
from ruamel.yaml.comments import CommentedSeq


def read_yaml(file_path: str) -> CommentedMap:
    """
    read yaml with comments by path
    :param file_path: path to file in filesystem
    :return: parsed high level CommentedMap
    """
    with open(file_path, "r") as file:
        yaml = ruamel.yaml.YAML()
        yaml.allow_unicode = True
        data = yaml.load(file)
    # Get comments associated with each key-value pair
    return data


def _remove_comment_from_yaml_string(value: str) -> str:
    """
    remove everything after symbol '#' if it exists
    """
    return value.split("#")[0]


def comment_remover(value: str) -> str:
    """
    parse input input string like a whole file with '\n' delimiters,
    remove everything after symbol '#' comment
    """
    lines: List[str] = list()
    for each_element in value.split("\n"):
        lines.append(_remove_comment_from_yaml_string(each_element))
    return "\n".join(lines)


def write_yaml(
    content: CommentedMap,
    dest_file: str,
    remove_comments=False,
) -> None:
    """
    write high level of CommentedMap, usually read from func:`~read_yaml`, into file
    :param content: body of the yaml
    :param dest_file: output path for writing CommentedMap in yaml format
    :param remove_comments: should be all comments removed ?
    """
    with open(dest_file, "w") as output_file:
        yaml_output = ruamel.yaml.YAML()
        yaml_output.preserve_quotes = False
        yaml_output.default_flow_style = True
        if remove_comments:
            yaml_output.dump(content, output_file, transform=comment_remover)
        else:
            yaml_output.dump(content, output_file)


def _get_comment_from_element(
    parent_element: Union[CommentedMap, CommentedSeq],
    key_name: Union[str, int],
) -> Union[str, None]:
    """
    get comment, if exists, from element
    :param parent_element: owner of the commented element
    :param key_name: number or name of the element inside parent_element
    :return: comment or None
    """
    if not hasattr(parent_element, "ca"):
        return None
    if key_name not in parent_element.ca.items:
        return None

    for each_index in range(len(parent_element.ca.items[key_name])):
        if parent_element.ca.items[key_name][each_index] is not None:
            return parent_element.ca.items[key_name][each_index].value.strip()[1:].strip()
    return None


def _remove_empty_values_seq(yaml_sequence: CommentedSeq) -> None:
    """
    remove empty elements, if no sub-elements left after filtering
    """
    to_remove: List[int] = list()
    for index in range(0, len(yaml_sequence)):
        if type(yaml_sequence[index]) == CommentedMap and len(yaml_sequence[index]) == 0:
            to_remove.append(index)
    to_remove.reverse()
    for key_for_removing in to_remove:
        yaml_sequence.pop(key_for_removing)


def _remove_empty_values_map(yaml_map: CommentedMap) -> None:
    """
    remove empty elements, that can appear after filtering
    """
    to_remove: List[str] = list()
    for each_item in yaml_map.items():
        yaml_key: str = each_item[0]
        yaml_value: object = each_item[1]
        if yaml_value == None or len(yaml_value) == 0:
            to_remove.append(yaml_key)
    for key_for_removing in to_remove:
        yaml_map.pop(key_for_removing)


def _walk_through_list_elements_remove_comments(
    content: CommentedSeq,
    current_path: List[str],
    white_comments: List[str],
):
    to_remove: List[int] = list()
    for each_item in range(0, len(content)):
        yaml_key: int = each_item
        yaml_value: object = content[each_item]
        yaml_comment: Union[str, None] = _get_comment_from_element(content, yaml_key)
        if yaml_comment is not None and yaml_comment not in white_comments:
            to_remove.append(yaml_key)
            continue
        if type(yaml_value) == str:
            continue
        if type(yaml_value) == CommentedMap:
            new_path: List = deepcopy(current_path)
            new_path.append(yaml_key)
            _walk_through_map_elements_remove_comments(yaml_value, new_path, white_comments)
            continue
        if type(yaml_value) == CommentedSeq:
            new_path: List = deepcopy(current_path)
            new_path.append(yaml_key)
            _walk_through_list_elements_remove_comments(yaml_value, new_path, white_comments)
            continue
        print(f"unknown type:{type(yaml_value)}")
    to_remove.reverse()
    for key_for_removing in to_remove:
        content.pop(key_for_removing)


def _walk_through_map_elements_remove_comments(
    content: CommentedMap,
    current_path: List[str],
    white_comments: List[str],
):
    to_remove: List[str] = list()
    for each_item in content.items():
        yaml_key: str = each_item[0]
        yaml_value: object = each_item[1]
        yaml_comment: Union[str, None] = _get_comment_from_element(content, yaml_key)
        if yaml_comment is not None and yaml_comment not in white_comments:
            to_remove.append(yaml_key)
            continue
        if type(yaml_value) == str:
            continue
        if type(yaml_value) == CommentedMap:
            new_path: List = deepcopy(current_path)
            new_path.append(yaml_key)
            _walk_through_map_elements_remove_comments(yaml_value, new_path, white_comments)
            _remove_empty_values_map(yaml_value)
            continue
        if type(yaml_value) == CommentedSeq:
            new_path: List = deepcopy(current_path)
            new_path.append(yaml_key)
            _walk_through_list_elements_remove_comments(yaml_value, new_path, white_comments)
            _remove_empty_values_seq(yaml_value)
            continue
        print(f"unknown type:{type(yaml_value)}")
    for key_for_removing in to_remove:
        content.pop(key_for_removing)


def _walk_through_list_elements_get_comments(
    content: CommentedSeq,
    current_path: List[str],
):
    return_value: Set[str] = set()
    for each_item in range(0, len(content)):
        yaml_key: int = each_item
        yaml_value: object = content[each_item]
        yaml_comment: Union[str, None] = _get_comment_from_element(content, yaml_key)
        if yaml_comment is not None:
            return_value.add(yaml_comment)

        if type(yaml_value) == str:
            continue
        if type(yaml_value) == CommentedMap:
            new_path: List = deepcopy(current_path)
            new_path.append(yaml_key)
            return_value.update(_walk_through_map_elements_get_comments(yaml_value, new_path))
            continue
        if type(yaml_value) == CommentedSeq:
            new_path: List = deepcopy(current_path)
            new_path.append(yaml_key)
            return_value.update(_walk_through_list_elements_remove_comments(yaml_value, new_path))
            continue
        print(f"unknown type:{type(yaml_value)}")
    return return_value


def _walk_through_map_elements_get_comments(
    content: CommentedMap,
    current_path: List[str],
):
    return_value: Set[str] = set()
    for each_item in content.items():
        yaml_key: str = each_item[0]
        yaml_value: object = each_item[1]
        yaml_comment: Union[str, None] = _get_comment_from_element(content, yaml_key)
        if yaml_comment is not None:
            return_value.add(yaml_comment)

        if type(yaml_value) == str:
            continue
        if type(yaml_value) == CommentedMap:
            new_path: List = deepcopy(current_path)
            new_path.append(yaml_key)
            return_value.update(_walk_through_map_elements_get_comments(yaml_value, new_path))
            continue
        if type(yaml_value) == CommentedSeq:
            new_path: List = deepcopy(current_path)
            new_path.append(yaml_key)
            return_value.update(_walk_through_list_elements_get_comments(yaml_value, new_path))
            continue
        print(f"unknown type:{type(yaml_value)}")
    return return_value


def remove_elements_with_comments(
    file_src: str,
    file_dst: str,
    white_labels: List[str],
    remove_comments=False,
) -> None:
    """
    read yaml file, parse it with comments,
    left only 'white-labeled' comments, remove the rest commented tags
    write result into destination file
    :param file_src: path to original yaml file with comments - comment is everything after '#' symbol
    :param file_dst: path to result yaml file
    :param white_labels: names of the comments that should be present in output file, other commented lines will be removed
    :param remove_comments: should output file have a comments ?
    """
    current_path: List[str] = list()
    yaml_file: object = read_yaml(file_src)
    _walk_through_map_elements_remove_comments(yaml_file, current_path, white_labels)
    write_yaml(yaml_file, file_dst, remove_comments=remove_comments)


def get_all_comments(file_src: str) -> Set[str]:
    """
    read file and retrieve all unique comments
    :param file_src: path to yaml file with comments
    :return: unique collection of comments
    """
    yaml_file: object = read_yaml(file_src)
    current_path: List[str] = list()
    return _walk_through_map_elements_get_comments(yaml_file, current_path)


if __name__ == "__main__":
    file_path = "test-data-01.yaml"
    yaml_file: CommentedMap = read_yaml(file_path)

    # yaml_file.ca.items["key1"][2].value
    print(_get_comment_from_element(yaml_file, "key1"))

    print(_get_comment_from_element(yaml_file, "key3"))

    # yaml_file["key3"]["key33"].ca.items[2][2].value
    print(_get_comment_from_element(yaml_file["key3"]["key33"], 2))

    # yaml_file["key3"]["key32"].ca.items["key322"][2].value
    print(_get_comment_from_element(yaml_file["key3"]["key32"], "key322"))

    remove_elements_with_comments(
        "test-data-01.yaml",
        "test-data-01-filtered.yaml",
        ["key31", "key2", "key23.3", "key33", "key4", "key42.2", "key42.3"],
        remove_comments=True,
    )

    comments: List[str] = list(get_all_comments("test-data-01.yaml"))
    comments.sort()
    print(comments)
