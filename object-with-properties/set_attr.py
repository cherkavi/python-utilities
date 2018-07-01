class CustomAttribute:
	
	def __init__(self):
		# avoid recursion
		super(CustomAttribute, self).__setattr__('data', dict())

	def __getattr__(self, prop_name):
		return self.data[prop_name]

	def __setattr__(self, prop_name, prop_value):
		self.data[prop_name] = prop_value

instance = CustomAttribute()

instance.p1 = "new value for property p1"
print(instance.p1)
try:
	print(instance.c2)
except KeyError as e:
	print("exception: " + str(e))

print(getattr(instance, "p1"))
print(dir(instance))