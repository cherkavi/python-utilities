from typing import List, Dict

def expand_dictionary(data: List[Dict[str,str]], delimiter: str, properties:List[str]):
    for each_property in properties:
        for each_data in data:
            if each_property not in each_data:
                continue
            value_for_parsing: str = each_data[each_property]
            if value_for_parsing is None:
                continue
            values:List[str] = value_for_parsing.split(delimiter)
            counter: int = 0
            for each_value in values:
                counter = counter + 1
                each_data[f"{each_property}_{counter}"] = each_value.strip() if each_value is not None else ""
            del each_data[each_property]


data:List[Dict[str, str]] = [
    {
        "prop1": 1,
        "text": "this,is,another,value",
        "another_text": "this is another value",
        "none_text": None
    }
]
expand_dictionary(data, ",", ["text", "another_text", "none_text"])
print(data)