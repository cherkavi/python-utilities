import sys
import hashlib
from typing import List

parameters:List[str] = list(filter(lambda x: len(x.strip())>0,  sys.argv[1:]))

if len(parameters)==1:
    print(hashlib.md5(f"Ashley Furniture{parameters[0]}".encode("utf-8")).hexdigest())
    exit(0)

if len(parameters)==2:
    print(hashlib.md5(f"{parameters[0]}{parameters[1]}".encode("utf-8")).hexdigest())
    exit(0)

