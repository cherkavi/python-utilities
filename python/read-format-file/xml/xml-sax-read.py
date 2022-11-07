import xml.sax

# create an XMLReader
parser = xml.sax.make_parser()
# turn off namepsaces
parser.setFeature(xml.sax.handler.feature_namespaces, 0)

# override the default ContextHandler
# Handler = MovieHandler()
# parser.setContentHandler( Handler )

class Handler(xml.sax.ContentHandler):
	def __init__(self):
		print("__init__")

	def startElement(self, tag, attributes):
		print("start-tag: %s attributes: %s " % (tag, attributes))

	def endElement(self, tag):
		print(" end -tag %s " % (tag))

	def characters(self, content):
		print(" content : " + content)


parser.setContentHandler(Handler())
xml_object = parser.parse("example.xml")
print(xml_object)