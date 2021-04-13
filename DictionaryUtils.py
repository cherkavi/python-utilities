import os.path

class DictionaryUtils(object):

    @staticmethod
    def readFromPropertyFile(pathToFile):
        """ property to map, property to dict, property file to dict 
        """
        if(pathToFile==None):
            return None
        if not os.path.isfile(pathToFile):
            return None
        myprops = {}
        with open(pathToFile, 'r') as f:
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
