# execute spark-shell with file, 
# file contains variables
# variable will be readed from command line during execution

import sys
import subprocess
from string import Template
import tempfile


def __clear_binary_line__(b_line):
    next_line = b_line.decode("utf-8")
    if next_line[len(next_line)-1] == "\n":
        next_line = next_line[:-1]
    return next_line.strip()


def replace_variables(file_name, variables):
	with open(file_name, "r") as input:
		file_data = input.read()
	
	temp_file = tempfile.NamedTemporaryFile(delete=False)
	temp_file.write(bytes(Template(file_data).substitute(variables), 'utf-8'))
	temp_file.flush()
	temp_file.close()
	return temp_file.name


def execute_spark_script(argument_holder):
    file_name = replace_variables(argument_holder[ArgumentHolder.__SCRIPT_FILE_NAME__], argument_holder)
    process = subprocess.Popen(["spark2-shell","--deploy-mode","client","-i",file_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    # process.stdin.write(":quit".encode("utf-8"))
    # process.stdin.close()
    return __clear_binary_line__(stdout)


class ArgumentHolder(dict):
    __SCRIPT_FILE_NAME__="__script_file_name__"

    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key]

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def has_key(self, k):
        return k in self.__dict__

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def pop(self, *args):
        return self.__dict__.pop(*args)

    def __cmp__(self, dict_):
        return self.__cmp__(self.__dict__, dict_)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

    def __unicode__(self):
        return unicode(repr(self.__dict__))

    @staticmethod
    def parse_arguments(arguments):
        instance = ArgumentHolder()
        if len(sys.argv)<2:
            print("at least filename should be specified")
            sys.exit(1)
        instance[ArgumentHolder.__SCRIPT_FILE_NAME__]=sys.argv[1]
        for index in range(0, int((len(sys.argv)-1)/2) ):
            instance[sys.argv[2+index*2].strip("--")]=sys.argv[2+index*2+1]
        return instance

def get_first_prefix(data, prefix):
    for each_line in data.split("\n"):
        if each_line.startswith(prefix):
            return each_line[len(prefix):]


if __name__=='__main__':
    output = execute_spark_script(ArgumentHolder.parse_arguments(sys.argv))
    print(get_first_prefix(output, "result: "))
