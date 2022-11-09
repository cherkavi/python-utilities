# misc

## DictionaryUtils

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/DictionaryUtils.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/DictionaryUtils.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## arguments

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/arguments.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/arguments.py -->
```py
def print_arguments_as_list(*input_arguments_as_list):
    for each_argument in input_arguments_as_list:
        print(each_argument)

print("----")
print_arguments_as_list("this", "is", "multipy", "arguments")


def print_arguments_as_map(**input_arguments_as_map):
    for each_argument in input_arguments_as_map:
        print(each_argument, input_arguments_as_map[each_argument])

print("----")
print_arguments_as_map(arg_1 = "this", arg_2 = "is", arg_3 = "multipy", arg_4 = "arguments")


def print_arguments_as_map(*input_arguments_as_list, **input_arguments_as_map):
    for each_argument in input_arguments_as_list:
        print(each_argument)
    for each_argument in input_arguments_as_map:
        print(each_argument, input_arguments_as_map[each_argument])

print("----")
print_arguments_as_map("this", "is", "multipy", "arguments", arg_1 = "this", arg_2 = "is", arg_3 = "multipy", arg_4 = "arguments")


# example of assignment of many elements
first_element, *rest_of_elements = [1,2,3,4,5]
print(first_element, rest_of_elements)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## array slicing

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/array-slicing.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/array-slicing.py -->
```py
pets=["dog", "cat", "bird", "pig"]
print pets[0:2]
print pets[:2]
print pets[:-1]
print pets[-3:]

# another example, with third parameter - step
print pets[0:4:2]
# step for range
print range(0,10)[::3]
print range(0,10)[::-1]
print range(0,10)[::-3]
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## base64

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/base64.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/base64.py -->
```py
import base64

print(base64.encodestring('login:password'.encode()))
print(base64.encodestring('weblogic:weblogic1'.encode()))


#               with open(path_to_image_file, "rb") as f:
#                   encoded = base64.b64encode(f.read())
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## browser open

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/browser-open.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/browser-open.py -->
```py
import webbrowser
# open string in browser
webbrowser.open("https://pyformat.info/");

# open local file in browser
#webbrowser.open('file://' + os.path.realpath(filename))
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## builder

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/builder.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/builder.py -->
```py
# return self, return itself, return this, type self, type itself, generic 
from __future__ import annotations

class Example:
  @staticmethod
  def build() -> Example:
    return Example()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## class abstract

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/class-abstract.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/class-abstract.py -->
```py
import abc
from abc import ABC

class Parent(ABC):

    @abc.abstractmethod
    def who_am_i(self):
        return "parent"


class Child(Parent):

    def who_am_i(self):
        return "child"

if __name__=="__main__":
    print(Child().who_am_i()) # child
    print( issubclass(Child, Parent) ) # True
    print( isinstance(Child(), Child) ) # True
    print( isinstance(Child(), Parent) ) # True
    print( isinstance(object(), Parent) ) # False
    # Parent() - can't create abstract class
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## clipboard

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/clipboard.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/clipboard.py -->
```py
from tkinter import Tk
import subprocess

def copy_to_clipboard(text: str):
    r = Tk()
    r.clipboard_clear()
    r.clipboard_append(text)
    r.update()
    r.destroy()

def open_in_browser(selected_url: str):
    subprocess.call(["x-www-browser", selected_url])
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## decorator with parameters

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/decorator-with-parameters.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/decorator-with-parameters.py -->
```py
#!/usr/bin/python -tt
class Wrapper(object):
    LIST_OF_WRAPPERS = list()

    def __init__(self, **kwargs):
        print("__init__", self, kwargs)
        self.path = kwargs['path']
        self.method = kwargs['method']
        Wrapper.LIST_OF_WRAPPERS.append(self)

    def __call__(self, external_function, *args, **kwargs):
    	print("__call__", external_function)

    	def real_decorator(*args, **kwargs):
    		new_value = ",".join([self.path, self.method, args[0]])
    		new_arguments_tuple = (new_value, )
    		return external_function(*new_arguments_tuple, **kwargs)

    	return real_decorator


@Wrapper(path="my new path", method="force")
def function_one(message):
    print("output function_one: " + message)


@Wrapper(path="my another path", method="peaceful")
def function_two(message):
    print("output function_two: " + message)

function_one("this is new message")
function_two("this is new message")
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## decorator

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/decorator.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/decorator.py -->
```py
#!/usr/bin/python -tt
class Wrapper(object):
    Reestr = list()

    def __init__(self, external_function):
        self.func = external_function
        Wrapper.Reestr.append(external_function) 

    def __call__(self):
        print ">>> call:", self.func.__name__, " of ", [x.__name__ for x in Wrapper.Reestr]
        self.func()
        print "<<< call", self.func.__name__

@Wrapper
def function_one():
    print "output function_one"

@Wrapper
def function_two():
    print "output function_two"

function_one()
function_two()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## default_parameter_list

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/default_parameter_list.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/default_parameter_list.py -->
```py
# default parameter list is working unexpectedly !!!!
class AnalyzeResult:
    # !!! don't do that, don't set default parameter list  !!!!
    def __init__(self, delete: bool, product_type: str = "variant", product_id: int = 0, variant_ids: List = list()):
        self._delete = delete
        self._product_type = product_type
        self._product_id = product_id
        self._variant_ids = variant_ids


class AnalyzeResult:
    def __init__(self, delete: bool, product_type: str = "variant", product_id: int = 0, variant_ids: List = None):
        self._delete = delete
        self._product_type = product_type
        self._product_id = product_id
        self._variant_ids = variant_ids if variant_ids is not None else list()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## dict comprehension

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/dict-comprehension.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/dict-comprehension.py -->
```py
# dictionary comprehension
# dict comprehension
a=["one", "two", "three"]
{full_name:full_name[0] for full_name in a }
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## dict comprehensive

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/dict-comprehensive.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/dict-comprehensive.py -->
```py
values = [9,7,6,3]
# inline conversion from list to dictionary
# dictionary comprehensive
squares = { each:each*each for each in values if each>0  }
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## dynamic class

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/dynamic-class.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/dynamic-class.py -->
```py
cls = type('my_class', (object,), {'__doc__': 'example of dynamically created class'})

print(cls)
print(cls.__doc__)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## dynamic vars

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/dynamic-vars.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/dynamic-vars.py -->
```py
def set_varibale_by_name(source:dict, name_of_variable_to_set:str, value):
    """ set variable by name, dynamically set variable
    """
    source[name_of_variable_to_set] = value
    # globals()[name_of_variable_to_set] = value

if __name__=="__main__":
    set_varibale_by_name(locals(), "a", 10)
    set_varibale_by_name(locals(), "b", "hello")

    print(a)
    print(b)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## elastic

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/elastic.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/elastic.py -->
```py
# pip install elasticsearch==7.10.1
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## else for

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/else-for.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/else-for.py -->
```py
#!/usb/bin/python
for i in range(10):
	try:
		if 10/i==2.0:
			break
	except ZeroDivisionError:
		print(1)
else:
	print(2)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## execute another script

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/execute-another-script.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/execute-another-script.py -->
```py
# execute another script from current program
os.system("my_script.py first_parameter second_parameter")
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## expand_dictionary

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/expand_dictionary.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/expand_dictionary.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## file extension

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/file-extension.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/file-extension.py -->
```py
import os

path = '/home/projects/sampledoc.docx'
root, extension = os.path.splitext(path)

print('Root:', root)
print('extension:', extension)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## find file

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/find-file.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/find-file.py -->
```py
import os

hash = "md5"
suffix = ".py"

hash_options = [hash[-len:]+suffix for len in range(len(hash)+1, 1, -1) ]
print(hash_options)
for file in os.listdir("."):
	for each_option in hash_options:
		if file.endswith(each_option):
			print(file)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## flatmap

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/flatmap.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/flatmap.py -->
```py
data = [ [1,2,3], [4,5,6], [7,8,9] ]

print( [each_element for each_line in data for each_element in each_line]  )
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## for else

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/for-else.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/for-else.py -->
```py
# for else
for each in range(5):
    print(each)
else:
    print("else without break")


for each in range(5):
    if each==3:
        break
    print(each)
else:
    print("else for break will never be")
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## function by name

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/function-by-name.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/function-by-name.py -->
```py
module = __import__('name_of_module')
func = getattr(module, 'function_name_inside_module')
func()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## generator

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/generator.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/generator.py -->
```py
print("example of inline generator")
inline_generator = (str(each) for each in range(1,5))
for i in inline_generator:
	print(i)

print("example of generator with 'yield'")
def my_generator(limit):
	values = range(1, limit+5)
	for x in values:
		if x%2==0:
			yield x
for i in my_generator(10):
	print(i)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## generic function

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/generic-function.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/generic-function.py -->
```py
T = TypeVar('T')
def get_value_or_else(parse_result: ParseResult, argument_name: str, default_value: T) -> T:
    return parse_result[argument_name] if argument_name in parse_result and parse_result[argument_name] else default_value
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## global_module

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/global_module.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/global_module.py -->
```py
import __builtin__
__builtin__.my_variable = 1
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## hash256

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/hash256.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/hash256.py -->
```py
import sys
import hashlib
my_string=f"Ashley Furniture{sys.argv[1]}"
print(hashlib.sha256(my_string.encode()).hexdigest())
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## hashmd5

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/hashmd5.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/hashmd5.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## http current date time

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/http-current-date-time.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/http-current-date-time.py -->
```py
#!/usr/bin/env python
import tornado.escape
import tornado.web
import tornado.ioloop
import time
import sys

class GetCurrentTimestamp(tornado.web.RequestHandler):
	def get(self):
		response=time.strftime("%Y%m%d%H%M%S")
		self.write(response)

application=tornado.web.Application([(r"/",GetCurrentTimestamp),])

if __name__=="__main__":
	if len(sys.argv)>1:
		application.listen(sys.argv[1])
	else:
		application.listen(9993)
	tornado.ioloop.IOLoop.instance().start()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## jupyter_utils

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/jupyter_utils.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/jupyter_utils.py -->
```py
from typing import List
import sys, paramiko
import os, subprocess
from typing import Dict


class AirflowBuilder:
    """
    collection of static methods for building request-body for Airflow REST API 
    """
    @staticmethod
    def auto_labeler(session_id: str, method: str)-> str:
        return '\'{"conf":{"session_id":"'+session_id+'","branch":"'+method+'"}}\''


class SshCommandExecutor:
    def __init__(self, host_name: str, user_name: str, user_pass: str):
        self.host_name = host_name
        self.user_name = user_name
        self.user_pass = user_pass

    def execute_command(self, command:str, print_error:bool = False) -> List[str]:
        """
        execute SSH command against remote host
        """
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.load_system_host_keys()
            ssh.connect(self.host_name, username=self.user_name, password=self.user_pass)
            # dir(ssh)
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
            if print_error:
                print(ssh_stderr.readlines())
            return [each_line.strip("\n") for each_line in ssh_stdout.readlines()]
        finally:
            ssh.close()

    def execute_airflow_dag(self, airflow_url:str, airflow_dag_name: str, airflow_user: str, airflow_pass: str, data_body: str) -> List[str]:
        """
        trig Airflow DAG 
        airflow_url = "https://airflow-stg.dplapps.advantagedp.org"
        data_body = '\'{"conf":{"session_id":"ed573f33-4103-47ba-b9ee-f424ec2f9313","branch":"run_labelers"} }\''
        print(executor.execute_airflow_dag(airflow_url, "auto_labelling", "label_search_depl-s", "passw", data_body))
        """
        url = f"{airflow_url}/api/experimental/dags/{airflow_dag_name}/dag_runs"
        airflow_pass_fixed='"'+airflow_pass+'"'
        command = f"curl --data-binary {data_body} -u {airflow_user}:{airflow_pass_fixed} -X POST {url}"
        print(airflow_user, airflow_pass_fixed, data_body)
        return self.execute_command(command)

    def maprfs_check_subfolder(self, path: str, deep_level: int, folder_name: str) -> List[str]:
        """
        check existence of subfolder by path on deep_level,
        Example:
        "/mapr/dp.prod.munich/ad-vantage/data/store/enriched/auto_labels/single", 5, "6ec6d14d-3e39-4bd2-a7f9-b646f7b96cd9"
        """
        return self.execute_command(f"find {path} -maxdepth {deep_level} -mindepth {deep_level} | grep {folder_name}")

    def maprfs_get_subfolders(self, path: str, deep_level: int) -> List[str]:
        """
        check existence of subfolder by path on deep_level,
        Example:
        "/mapr/dp.prod.munich/ad-vantage/data/store/enriched/auto_labels/single", 5
        """
        return self.execute_command(f"find {path} -maxdepth {deep_level} -mindepth {deep_level}")

    def elastic_records_by_session(self, url:str, index_name: str, session_id: str) -> List[str]:
        command = f'curl --silent -X GET "{url}/{index_name}/_count?q=sessionId:{session_id}" | jq ".count"'
        return self.execute_command(command)


def get_first_record(list_of_string: List[str])->str:
    if len(list_of_string)>0:
        return list_of_string[0]
    else:
        return ""


def get_last_subfolder(full_path: str)->str:
    marker = full_path.rfind("/")
    return full_path[marker+1:] if marker>0 else ""


def parse_login(var_name:str) -> str:
    dirty_value:str = var_name[len("USER_"):]
    last_underscore_position = dirty_value.rfind("_")
    if last_underscore_position>0:
        return dirty_value[:last_underscore_position]+"-"+ (dirty_value[last_underscore_position+1:] if len(dirty_value)>(last_underscore_position+1) else "")
    else:
        return dirty_value


def parse_passw(var_passw: str) -> str:
    return var_passw[1:].strip("\"")


def parse_users_from_env()-> Dict[str, str]:
    return_value: Dict[str, str] = dict()
    for each_value in str(subprocess.check_output("env")).split("\\n"):
        if each_value.startswith("USER_"):
            env_var_first_part = each_value.split("=")[0]
            return_value[parse_login(env_var_first_part)]=parse_passw(each_value[len(env_var_first_part):])
    return return_value


list_of_users = parse_users_from_env()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## mail send

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/mail-send.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/mail-send.py -->
```py
import smtplib
from email.mime.text import MIMEText

#with open(textfile, 'rb') as fp:
    # Create a text/plain message
#    msg = MIMEText(fp.read())

msg = MIMEText("simple text message ")
msg['Subject'] = 'just a subject'
msg['From'] = "vitali.cherkashyn@localhost.com"
msg['To'] = "vitali.cherkashyn@vodafone.com"


# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP('localhost:2525')
s.sendmail("vitali.cherkashyn@localhost.com", ["vitali.cherkashyn@vodafone.com"], msg.as_string())
s.quit()


import yagmail
yag = yagmail.SMTP(user=mail_login, password=mail_password)
yag.send('somename@somewhere.com', subject = None, contents = 'Hello')
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## md5 example

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/md5-example.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/md5-example.py -->
```py
from hashlib import md5 as md5

def generate_signature(user, password, date):
    user_password_hash = md5("%s/%s" % (user, password)).hexdigest().upper()
    signature = md5("%s%s" % (date, user_password_hash)).hexdigest().upper()
    return signature

print(generate_signature("U20005", "1234", "2016-10-22T22:25:28+03:00"))
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## md5

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/md5.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/md5.py -->
```py
#!/usr/bin/python

# python 2.7.x 
# import md5 as md5hash from md5
# print(md5("hello"))

# python 3.5.x
import hashlib
hashlib.md5(open('/home/technik/projects/temp/ista/json-source/2018110815330826780340100-2018110815330829280340100-956.json','rb').read().encode("utf-8")).hexdigest()

hashlib.md5(b"hello").hexdigest()
brand="temp"
sku="my_code"
hashlib.md5(f"{brand}{sku}".encode("utf-8")).hexdigest()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## method_by_name

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/method_by_name.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/method_by_name.py -->
```py
class Foo:
    def bar1(self):
        print(1)
    def bar2(self):
        print(2)

def call_method(o, name):
    return getattr(o, name)()


f = Foo()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## module attributes check

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/module-attributes-check.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/module-attributes-check.py -->
```py
import settings

def check_mandatory_attributes(object_with_attributes, list_of_attributes: List[str]):
    for each_attribute in list_of_attributes:
        if getattr(object_with_attributes, each_attribute, None) is None:
            print(f"mandatory attribute should be present as ENV variable {each_attribute}")
            exit(1)

check_mandatory_attributes(settings, ["DATAAPI_BASE_URL","DATAAPI_API_KEY","DATAAPI_ACCOUNT_ID","DATAAPI_CONTEXT_ID","DATAAPI_CONTEXT","AWS_ACCESS_KEY_ID","AWS_SECRET_ACCESS_KEY","AWS_REGION","AWS_S3_BUCKET_NAME","AIRFLOW_URL","AIRFLOW_USER","AIRFLOW_PASSWORD"])
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## multi argument for

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/multi-argument-for.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/multi-argument-for.py -->
```py
#!/usr/bin/python -tt
animals = ["cat", "dog", "pig", "rabbit"]
for index, value in enumerate(animals):
	print "index: {}  value: {}".format(index,value)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## multiply inheritance

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/multiply-inheritance.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/multiply-inheritance.py -->
```py
import abc
from abc import ABC

class Vehicle(ABC):
    def __init__(self, name: str):
        self._name = name

    def who_am_i(self):
        print(f"vehicle: {self._name}  {self}")

class Car(Vehicle):
    def __init__(self, name: str, wheels: int):
        super().__init__(name)
        self._wheels: int = wheels
        print(">> init car")

    def __str__(self):
        return f"{self._name} {self._wheels}"

    def who_am_i(self):
        print(f"car: {self._name}  {self}")

class Boat(Vehicle):
    def __init__(self, name: str, wheels: int):
        super().__init__(name)
        self._motors = wheels
        print(">> init boat")

    def __str__(self):
        return f"{self._name} {self._motors}"

    def who_am_i(self):
        print(f"boat: {self._name}  {self}")        

# example of multiply inheritance
class SwimmingCar(Car, Boat):
    def __init__(self):
        super().__init__("ford", wheels=4)        


vechicle:SwimmingCar = SwimmingCar()
vechicle.who_am_i()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## named tuple

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/named-tuple.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/named-tuple.py -->
```py
from collections import namedtuple

CustomComputer = namedtuple("Computer", ["keyboard", "mouse", "monitor"])
my_computer = CustomComputer("Apple", "Logitech", ["Dell", "Dell", "NEC", "Built-in"])

# pay attention, namedtuple - CustomComputer, but class - Computer
print(my_computer) # Computer(keyboard='Apple', mouse='Logitech', monitor=['Dell', 'Dell', 'NEC', 'Built-in'])
# unpack parameters
print(*my_computer)    # Apple Logitech ['Dell', 'Dell', 'NEC', 'Built-in']
(my_keyboard, my_mouse, my_monitor) = my_computer
print(my_keyboard, my_mouse, my_monitor) # Apple Logitech ['Dell', 'Dell', 'NEC', 'Built-in']
# print fields by index
print(my_computer[0])  # Apple
print(my_computer[1])  # Logitech
print(my_computer[2])  # ["Dell", "Dell", "NEC", "Built-in"]
# print fields by name 
print(my_computer.keyboard) # Apple
print(my_computer.mouse)    # Logitech
print(my_computer.monitor)  # ["Dell", "Dell", "NEC", "Built-in"]


# extension
CustomNotebook = namedtuple("Notebook", CustomComputer._fields + ('battery', ))
print(CustomNotebook)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## object copy

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/object-copy.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/object-copy.py -->
```py
# shallow copy 
a = {1: [1,2,3]}
b = a.copy()
a[1].append(4)
print(a)
# {1: [1, 2, 3, 4]}
print(b)
# {1: [1, 2, 3, 4]}


import copy
# deep copy
a = {1: [1,2,3]}
b = copy.deepcopy(a)
a[1].append(4)
print(a)
# {1: [1, 2, 3, 4]}
print(b)
# {1: [1, 2, 3]}
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## operator override

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/operator-override.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/operator-override.py -->
```py
# example of overriding operators
# operator overriding
class Value:
    def __init__(self, value):
        self.value = value

    # - __sub__, * __mul__, ** __pow__, / __truediv__, // __floordiv__, % __mod__
    # << __lshift__, >> __rshift__, & __and__, | __or__, ^ __xor__, ~ __invert__
    # < __lt__, <= __le__, == __eq__, != __ne__, > __gt__, >= __ge__
    def __add__(self, other):
        return Value(" -[ "+self.value +" ]-  -[ "+ other.value+" ]- ")

    def __str__(self):
        return self.value


v1 = Value("line#1")
v2 = Value("line#2")
print(v1 + v2)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## os package

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/os-package.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/os-package.py -->
```py
#!/usr/bin/env python

# example to send signal to current process.

import os
import signal
import sys
import syslog
import time

# send signal to current process
signal.signal(signal.SIGHUP, signal.SIG_IGN)


class SignalListener:
    """
    listen shutdown signal from Operation System
    """
    def __init__(self):
        self.shutdown = False
        signal.signal(signal.SIGINT, self._process_shutdown)
        signal.signal(signal.SIGTERM, self._process_shutdown)

    def _process_shutdown(self, signum, frame):
        self.shutdown = True
        logger = logging.getLogger(self.__class__.__name__)
        logger.info("shutdown !!! ")
        

# pid id of current process
os.getpid()

# pid of parent process
os.getppid()

# run child process
os.spawnv(os.P_WAIT, path, args)

# execute external program with replacing current process
os.execv(to_launch[0], to_launch)

# write data into syslog 
syslog.syslog(syslog.LOG_ERR, str(sys.exc_info()))
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## os signal

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/os-signal.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/os-signal.py -->
```py
import os, sys
import time
import signal
def func(signum, frame):
    print 'You raised a SigInt! Signal handler called with signal', signum

signal.signal(signal.SIGINT, func)
while True:
    print "Running...",os.getpid()
    time.sleep(2)
    os.kill(os.getpid(),signal.SIGINT)


##############################################################

import signal  
import time  
 
# Our signal handler
def signal_handler(signum, frame):  
    print("Signal Number:", signum, " Frame: ", frame)  
 
def exit_handler(signum, frame):
    print('Exiting....')
    exit(0)
 
# Register our signal handler with `SIGINT`(CTRL + C)
signal.signal(signal.SIGINT, signal_handler)
 
# Register the exit handler with `SIGTSTP` (Ctrl + Z)
signal.signal(signal.SIGTSTP, exit_handler)


signal.signal(signal.SIGHUP, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGQUIT, signal_handler)
signal.signal(signal.SIGILL, signal_handler)
signal.signal(signal.SIGTRAP, signal_handler)
signal.signal(signal.SIGABRT, signal_handler)
signal.signal(signal.SIGBUS, signal_handler)
signal.signal(signal.SIGFPE, signal_handler)
#signal.signal(signal.SIGKILL, signal_handler)
signal.signal(signal.SIGUSR1, signal_handler)
signal.signal(signal.SIGSEGV, signal_handler)
signal.signal(signal.SIGUSR2, signal_handler)
signal.signal(signal.SIGPIPE, signal_handler)
signal.signal(signal.SIGALRM, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# While Loop
while 1:  
    print("Press Ctrl + C") 
    time.sleep(3)


###########################################################
def register_signals(self) -> None:
        """Register signals that stop child processes"""
        signal.signal(signal.SIGINT, self._exit_gracefully)
        signal.signal(signal.SIGTERM, self._exit_gracefully)
        signal.signal(signal.SIGUSR2, self._debug_dump)

    def _exit_gracefully(self, signum, frame) -> None:
        sig_name = signal.Signals(signum).name
        
        """Helper method to clean up processor_agent to avoid leaving orphan processes."""
        if not _is_parent_process():
            # Only the parent process should perform the cleanup.
            return
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## partial

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/partial.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/partial.py -->
```py
# partial function
from functools import partial
def func(u,v,w,x):
    return u*4 + v*3 + w*2 + x

another_function = partial(func, 1,2,3)

print(another_function(4))
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## pip manage

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/pip-manage.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/pip-manage.py -->
```py
# https://bootstrap.pypa.io/get-pip.py
# python get-pip.py
import pip
pip.main(['install', 'stem']) # install package
# pip.main(['install', '-U', 'requests']) # update package
# pip.main(['uninstall ', '-y', 'requests']) # uninstall package
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## port check

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/port-check.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/port-check.py -->
```py
import socket
import sys
from contextlib import closing


def check_port(host, port_number):
   with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(1)
        if sock.connect_ex((host, int(port_number))) == 0:
            print("%s : %s  >>open<<" % (host, port_number))
        else:
            print("%s : %s  NOT open" % (host, port_number))


if __name__=='__main__':
    check_port(sys.argv[1], sys.argv[2])
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## print to error

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/print-to-error.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/print-to-error.py -->
```py
import sys

print ("standard output ")
print ("standard output ", file=sys.stdout)
# System.err, stderror, error output
print ("output to error ", file=sys.stderr)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## private memeber

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/private-memeber.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/private-memeber.py -->
```py
class Car:
  __wheel = 4
  
c = Car()
print(c._Car__wheel)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## process kill

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/process-kill.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/process-kill.py -->
```py
import psutil

PROCNAME = "python.exe"

for proc in psutil.process_iter():
    # kill process
    if proc.name() == PROCNAME:
        proc.kill()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## random

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/random.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/random.py -->
```py
# random example
import random
# This command returns a floating point number, between 0 and 1.
print(random.random())

# It returns a floating point number between the values given as X and Y.
print(random.uniform(10, 20))

# This command returns a random integer between the values given as X and Y.
print(random.randint(20, 30))
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## range

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/range.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/range.py -->
```py
# range - return list
print(sum(range(1,100)))
# xrange - return iterator
print(sum(xrange(1,100)))
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## return_None_or_str

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/return_None_or_str.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/return_None_or_str.py -->
```py
from types import UnionType


def my_func(a:int) -> UnionType[None, str]:
    if a>10:
        return "big"
    else:
        return None
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## spark command line document here

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/spark-command-line-document-here.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/spark-command-line-document-here.py -->
```py
# orc folder record counter
# subprocess.check_output(["spark2-shell", "--deploy-mode", "client", "<<<", "MARKER_END_DOCUMENT", ":quit", "MARKER_END_DOCUMENT"])
# hdfs dfs -ls /processed/datateam/ingestor_v5/cfb72a80-ec76-43dc-af72-7458c2f40fcb/Can
# val myDataFrame = spark.read.orc("/processed/datateam/ingestor_v5/cfb72a80-ec76-43dc-af72-7458c2f40fcb/Can") 
# val result = myDataFrame.count()

import sys
import subprocess
import os
import stat


def execute_line(command_line):
	file_name = "1.sh"
	out_file = "out.txt"
	with open(file_name, "w") as output:
		output.write(command_line+" > "+out_file)
	os.chmod(file_name, stat.S_IRWXU | stat.S_IRWXG)
	subprocess.check_output(["bash", file_name], shell=False).decode("utf-8")
	os.remove(file_name)
	with open(out_file, "r") as input:
		lines = list(map(lambda each_line: each_line.strip(), input.readlines()))
		return_value = list( filter(lambda each_line: len(each_line)>0, lines) )
	os.remove(out_file)
	return return_value


if __name__=="__main__":
	# find path to session by id: 
	if len(sys.argv)<2:
		print("session name should be specified")
		sys.exit(1)
	hdfs_command = """hdfs dfs -ls /processed/datateam/ingestor_v5/%s/ | awk '{print $8}'""" % sys.argv[1]	
	folders = execute_line(hdfs_command)

	folders_list = "%s" % folders
	scala_script = """
spark2-shell --deploy-mode client << MARKER_END_DOCUMENT
var counter:Long = 0
val folders = Seq(%s)
for(each_folder<-folders){
	var folder = each_folder.trim()
	if(folder.length()!=0) {
		println(each_folder)
		var frame = spark.read.format("orc").load(each_folder)
		var current_counter = frame.count	
		println(">"+current_counter+"<")
		counter = counter+current_counter
	}
}
println(">>>"+counter+"<<<")
:quit
MARKER_END_DOCUMENT
	""" % folders_list[1:-1].replace("'","\"")
	scala_script_file = "out.scala"
	with open(scala_script_file, "w") as output:
		output.write(scala_script)
	print(scala_script)
	out = subprocess.check_output(["spark2-shell", "--deploy-mode", "client", "<<<", "MARKER_END_DOCUMENT", ":quit", "MARKER_END_DOCUMENT"])
	print(out)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## spark command line wrapper

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/spark-command-line-wrapper.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/spark-command-line-wrapper.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## sql file processor

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/sql-file-processor.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/sql-file-processor.py -->
```py
#!/usr/bin/python -tt
import sys
import string
from string import join



if len(sys.argv) <= 1:
    print("file name should be specified")
    sys.exit(1)

parameters = list()
with open(sys.argv[1]) as f:
    for each_line in f:
        index = each_line.find("--")
        each_line=each_line[:(index-1)]
        parameters.append(each_line)

print(join(parameters, " "))
print()
for parameter in parameters:
    each=parameter.strip()
    if each.endswith(","):
        each=each[0:len(each)-1]
    index = each.index(".")
    if index >= 0:
        print(each[index+1:])
    else:
        print (each)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## str repr

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/str-repr.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/str-repr.py -->
```py
import datetime 
today = datetime.datetime.now() 

# "official" string representation - all information about object, mostly for debugging
# Prints readable format for date-time object 
print(str(today))

# prints the official format of date-time object 
# "informal" information
print(repr(today))
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## string regexp

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/string-regexp.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/string-regexp.py -->
```py
import re
name="Azita M. Mojarad"

re.sub("[^a-z]","-", name)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## string validation

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/string-validation.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/string-validation.py -->
```py
# https://regex101.com/
#

import re
pattern=r"[1,8,9]{1}[0-9]{7}"
re.match(pattern, "15554449")
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## string2byte

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/string2byte.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/string2byte.py -->
```py
# To convert a string to bytes.
data = b"this is string" 			#bytes
data = "this is string".encode()	#bytes

data = b"".decode() #string
data = str(b"")  	#string
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## string_remove_after_last

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/misc/string_remove_after_last.py) -->
<!-- The below code snippet is automatically added from ../../python/misc/string_remove_after_last.py -->
```py
print(".".join(df.split('.')[:-1]))
```
<!-- MARKDOWN-AUTO-DOCS:END -->


