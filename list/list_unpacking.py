from typing import List
from typing import Union

# multi type declaration 
def get_names(prefix: str, names: Union[str, List]) -> Union[str, List]:    
    if isinstance(names, List):
        return [prefix+each_name for each_name in names]
    else:
        return prefix+names

# unpacking 
a,b = get_names("___", ["one", "two"])
c = get_names("___", "figure")

print(a,b,c)
