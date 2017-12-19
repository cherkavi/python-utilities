import configparser, sys, os, json
import tornado.ioloop, tornado.web

endpoint_list = "/list";
endpoint_file = "/file/"

class SourceFolder:
	def __init__(self, path_to_folder, nodes):
		file_list = read_from_folder(path_to_folder)
		for each_node in nodes:
			file_list = file_list + read_from_node(each_node)		 
		self.files = [subfolder_files for subfolder_files in file_list]
		self.index = -1

	def read_from_folder(self, path):
		try:
			return os.listdir(path_to_folder)
		except:
			return []

	def read_from_node(self, url):
		return []		

	def __iter__(self):
		return self

	def __next__(self):
		self.index = self.index + 1
		if self.index >= len(self.files):
			raise StopIteration()
		else:
			return self.files[self.index]		


class ListHandler(tornado.web.RequestHandler):

	def initialize(self, folder):
		self.folder = folder

	def get(self):
		self.write( json.dumps([each for each in SourceFolder(self.folder)]) )


def main(ini_file):
	config = configparser.ConfigParser()
	config.read(ini_file)
	folder = config["local"]["folder"]
	nodes = [ each.strip() for each in config["remote"]["nodes"].split(",")]
	app = tornado.web.Application([ (endpoint_list, ListHandler, dict(folder=folder)), ])
	app.listen(9090)
	tornado.ioloop.IOLoop.current().start()


if __name__=="__main__":
	main(sys.argv[1])