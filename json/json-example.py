import json

example = {"a":10, "b":20}
print(json.dumps(example))
print(json.loads(json.dumps(example)))


class Example:
    def __init__(self, value):
    	self.value = value

    def __str__(self):
    	return self.value

# is not JSON serializable - using pickle
#print(json.dumps(Example("hello")))