# json document print all the elements in xpath style
import json

def walk_leaves(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            new_path = f"{path}.{k}" if path else k
            walk_leaves(v, new_path)
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            new_path = f"{path}[{idx}]"
            walk_leaves(item, new_path)
    else:
        print(f"{path}: {obj}")

# your JSON document
with open('1.json') as f:
    data = json.load(f)

walk_leaves(data)
