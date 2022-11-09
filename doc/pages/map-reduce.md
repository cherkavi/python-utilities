# map-reduce

## UserSessionCounter

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/map-reduce/UserSessionCounter.py) -->
<!-- The below code snippet is automatically added from ../../python/map-reduce/UserSessionCounter.py -->
```py
from mrjob.job import MRJob

class UserSessionCounter(MRJob):

    def mapper(self, key, line):
        (id_visitor, id_session, *rest) = line.split("|")
        if len(id_visitor)==0 or id_visitor == 'id_visitor':
            return
        yield id_visitor, 1

    def reducer(self, id_visitor, occurences):
        yield id_visitor, sum(occurences)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## UserSessionCounterRunner

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/map-reduce/UserSessionCounterRunner.py) -->
<!-- The below code snippet is automatically added from ../../python/map-reduce/UserSessionCounterRunner.py -->
```py
from UserSessionCounter import UserSessionCounter

class RemoteFileAware:
    def __init__(self, url, local_path):
        self.filepath = local_path
        RemoteFileAware.download_file(url, local_path)

    def __enter__(self):
    	pass

    def __exit__(self):
        import shutil
        shutil.remove(self.filepath)

    @staticmethod
    def download_file(url, local_file):
        import requests, shutil
        response = requests.get(url, stream=True)
        with open(local_file, "wb") as output_file:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, output_file)


if __name__ == '__main__':
    local_file = "data.txt"
    remote_file = "https://raw.githubusercontent.com/curran/data/gh-pages/airbnb/airbnb_session_data.txt"

    with RemoteFileAware(remote_file, local_file) as _:
	    instance = UserSessionCounter([local_file])
	    with instance.make_runner() as runner:
	        user_counter = 0
	        leader = {'name':"", 'size': 0}
	        runner.run()
	        for line in runner.stream_output():
	            (id_visitor, count) = instance.parse_output_line(line)
	            # print(id_visitor, count)
	            user_counter = user_counter + 1
	            if leader['size']<count:
	                 leader['size'] = count
	                 leader['name'] = id_visitor
	        print("amount of users: ", user_counter)
	        print("leader : %s " % (leader))
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## combiner

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/map-reduce/combiner.py) -->
<!-- The below code snippet is automatically added from ../../python/map-reduce/combiner.py -->
```py
import sys

def main():
    last_key = None
    count = 0
    size = 0

    def print_values():
        print(last_key + "\t" + str(size)+";"+str(count))

    for each_line in sys.stdin:
        key_value = each_line.strip().split("\t")
        if len(key_value)<2:
            continue
        key = key_value[0]
        size_count = key_value[1].split(";")
        key_size = int(size_count[0])
        key_count = int(size_count[1])

        if key!=last_key:
            if last_key:
                print_values()
            count = key_count
            size = key_size
            last_key = key
        else:
            count += key_count
            size = size+key_size

    print_values()



if __name__ == '__main__':
    main()
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## reducer

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/map-reduce/reducer.py) -->
<!-- The below code snippet is automatically added from ../../python/map-reduce/reducer.py -->
```py
import sys

def main():
    last_key = None
    count = 0
    size = 0

    def print_values():
        print(last_key + "\t" + str(int(size/count)))

    for each_line in sys.stdin:
        key_value = each_line.strip().split("\t")
        if len(key_value)<2:
            continue
        key = key_value[0]
        value = key_value[1]

        if key!=last_key:
            if last_key:
                print_values()
            count=1
            size = int(value)
            last_key = key
        else:
            count+=1
            size = size+int(value)

    print_values()



if __name__ == '__main__':
    main()
```
<!-- MARKDOWN-AUTO-DOCS:END -->


