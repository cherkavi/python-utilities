import shelve


class Example:
    def __init__(self, value):
    	self.value = value

    def __str__(self):
    	return self.value

database = shelve.open("my-db-file")


database["simple_string"] = "this is simple string into DB"
database["int_value"] = 5
database["complex_value"] = Example("this is simple object") 

database.close()

# open existing
db = shelve.open("my-db-file")
print(db["simple_string"])
print(db["int_value"])
print(db["complex_value"])

# delete key
del db["int_value"]

# print all keys
print(db.keys())