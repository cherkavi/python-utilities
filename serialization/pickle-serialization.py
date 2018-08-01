import pickle

class Example:
    def __init__(self, value):
    	self.value = value

    def __str__(self):
    	return self.value


# serialization into file
with open('filename', 'wb') as external_file:
    pickle.dump(Example("hello"), external_file)

# var2 = # should implement def write 
# pickle.dump("hello string", var2)

# deserialization from file
with open('filename','rb') as f:
    var = pickle.load(f)
    print(var)
    print(type(var))