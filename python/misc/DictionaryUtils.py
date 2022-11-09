import os.path
from typing import Dict

class DictionaryUtils(object):

    @staticmethod
    def property_to_dict(path_to_file: str) -> Dict:
        """ property to map, property to dict, property file to dict 
        """
        if(path_to_file==None):
            return None
        if not os.path.isfile(path_to_file):
            return None
        myprops = {}
        with open(path_to_file, 'r') as f:
            for line in f:
                #removes trailing whitespace and '\n' chars
                line = line.rstrip()

                #skips blanks and comments w/o =
                if "=" not in line :
                    continue
                #skips comments which contain =
                if line.startswith("#") :
                    continue

                k, v = line.split("=", 1)
                myprops[k] = v
        return myprops


    @staticmethod
    def property_to_string(path_to_file: str, separator: str = " ") -> str:
        """ property to map, property to dict, property file to dict 
        """
        if(path_to_file==None):
            return None
        if not os.path.isfile(path_to_file):
            return None
        return_value = []
        with open(path_to_file, 'r') as f:
            for line in f:
                #removes trailing whitespace and '\n' chars
                line = line.rstrip()

                #skips blanks and comments w/o =
                if "=" not in line :
                    continue
                #skips comments which contain =
                if line.startswith("#") :
                    continue

                k, v = line.split("=", 1)
                return_value.append(f"{k}={v}")
                myprops[k] = v
        return separator.join(return_value)
