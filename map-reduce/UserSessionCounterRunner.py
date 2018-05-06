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
