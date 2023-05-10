import re
from typing import List 

def find_embraced_occurrences(text: str, brace_start: str, brace_end: str) -> List[str]:
    # Define a regular expression pattern to match text between braces
    pattern = r'{(.+?)}'
    
    # Replace the brace characters in the pattern with the ones provided as input
    pattern = pattern.replace('{', re.escape(brace_start)).replace('}', re.escape(brace_end))

    # Use re.findall to find all occurrences of the pattern surrounded by braces in the string
    matches = re.findall(pattern, text)
    
    # Return the list of matches
    return matches

string = "The {quick} brown {fox} jumped over the {lazy} dog."
occurrences = find_embraced_occurrences(string, "{","}")
print(occurrences) 

string = "The [quick] brown [fox] jumped over the [lazy] dog."
occurrences = find_embraced_occurrences(string, "[", "]")
print(occurrences) 

string = "The [[quick]] brown [[fox]] jumped over the [[lazy]] dog."
occurrences = find_embraced_occurrences(string, "[[", "]]")
print(occurrences) 

print(string[:string.index("[[")])


