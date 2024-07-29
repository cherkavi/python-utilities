import sys
from typing import List
import random


def read_file_into_list(filename, delimiter='---'):
  with open(filename, 'r') as file:
    data = file.read()
    elements = data.split(delimiter)
    return elements

def read_value(file_name:str) -> int:
  try:
    with open(file_name, 'r') as f:
        return int(f.read())
  except:    
    return 0
  
def write_value(file_name:str, value: int):
    with open(file_name, 'w') as f:
      f.write(str(value))


if __name__ == '__main__':
  arguments:List = sys.argv[1:]
  if len(arguments)==0:
    print("file with text delimited by --- should be specified", file=sys.stderr)
    sys.exit(1)
  file_text:str = arguments[0]
  file_counter:str = arguments[1] if len(arguments)>1 else None
  elements: List[str] = read_file_into_list(file_text)
  if not file_counter:
    print(elements[random.randint(0, len(elements))].strip())
  else: 
    counter = read_value(file_counter)
    print(elements[counter])
    counter = counter + 1
    write_value(file_counter, counter)
