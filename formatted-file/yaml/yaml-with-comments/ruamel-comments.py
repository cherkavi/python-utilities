# pip install ruamel.yaml
# 
from ast import Dict
from copy import deepcopy
from os import write
from typing import List, Union
import ruamel.yaml
from ruamel.yaml.comments import CommentedMap 

def read_yaml(file_path: str) -> CommentedMap:
    with open(file_path, 'r') as file:
        yaml = ruamel.yaml.YAML()
        data = yaml.load(file)
    # Get comments associated with each key-value pair
    return data

def write_yaml(content: CommentedMap, dest_file: str) -> None:
    with open(dest_file, "w") as output_file:
        ruamel.yaml.dump(content, output_file)

def get_comment(parent_element: CommentedMap, key_name: Union[str,int]) -> Union[str, None] : 
    if not hasattr(parent_element, "ca"):
        return None
    if key_name not in parent_element.ca.items:
        return None
    
    for each_index in range(len(parent_element.ca.items[key_name])):
        if parent_element.ca.items[key_name][each_index] is not None:
            return parent_element.ca.items[key_name][each_index].value.strip()
    return None


def walk_through_elements_remote_comments(content: CommentedMap, current_path: List[str], white_comments:List[str]):
    to_remove: List[str] = list()
    for each_item in content.items():
        yaml_key: str = each_item[0]
        yaml_value: object = each_item[1]
        yaml_comment: Union[str, None] = get_comment(content, yaml_key)
        if yaml_comment is not None and yaml_comment not in white_comments:
            continue
        if type(yaml_value)==CommentedMap:
            new_path:List = deepcopy(current_path)
            new_path.append(yaml_key)
            walk_through_elements_remote_comments(yaml_value, new_path, white_comments)
    for key_for_removing in to_remove:
        content.pop(key_for_removing)


def remove_elements_with_comments(file_src: str, file_dst: str, white_labels: List[str]) -> None:
    current_path:List[str] = list()
    yaml_file: object = read_yaml(file_src)
    walk_through_elements_remote_comments(yaml_file, current_path, white_labels)
    write_yaml(yaml_file, file_dst)


if __name__=='__main__':
    file_path = 'test-data-01.yaml'
    yaml_file: CommentedMap= read_yaml(file_path)
    print(yaml_file)
    

    # yaml_file.ca.items["key1"][2].value
    print(get_comment(yaml_file, "key1"))

    print(get_comment(yaml_file, "key3")) 

    # yaml_file["key3"]["key33"].ca.items[2][2].value    
    print(get_comment(yaml_file["key3"]["key33"], 2)) 

    # yaml_file["key3"]["key32"].ca.items["key322"][2].value    
    print(get_comment(yaml_file["key3"]["key32"], "key322"))

    remove_elements_with_comments('test-data-01.yaml', 'test-data-01-filtered.yaml', ['key31', 'key23.3'])
