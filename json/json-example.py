import json

example = {"a":10, "b":20}
# convert to json string
print(json.dumps(example))
# convert to json string and then move back to object 
#              - read from string
print(json.loads(json.dumps(example)))


class Example:
    def __init__(self, value):
    	self.value = value

    def __str__(self):
    	return self.value

# is not JSON serializable - using pickle
#print(json.dumps(Example("hello")))
