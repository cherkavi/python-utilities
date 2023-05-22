# pip install ruamel.yaml
# 
from typing import Union
import ruamel.yaml

def read_yaml(file_path: str):
    with open(file_path, 'r') as file:
        yaml = ruamel.yaml.YAML()
        data = yaml.load(file)

    # Get comments associated with each key-value pair
    return data

def get_comment(parent_element: object, key_name: Union[str,int]) -> Union[str, None] : 
    if not hasattr(parent_element, "ca"):
        return None
    if key_name not in parent_element.ca.items:
        return None
    
    for each_index in range(len(parent_element.ca.items[key_name])):
        if parent_element.ca.items[key_name][each_index] is not None:
            return parent_element.ca.items[key_name][each_index].value.strip()
    return None

    


if __name__=='__main__':
    file_path = 'test-data-01.yaml'
    yaml_file = read_yaml(file_path)
    print(yaml_file)
    

    # yaml_file.ca.items["key1"][2].value
    print(get_comment(yaml_file, "key1"))

    print(get_comment(yaml_file, "key3")) 

    # yaml_file["key3"]["key33"].ca.items[2][2].value    
    print(get_comment(yaml_file["key3"]["key33"], 2)) 

    # yaml_file["key3"]["key32"].ca.items["key322"][2].value    
    print(get_comment(yaml_file["key3"]["key32"], "key322"))
