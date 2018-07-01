class CustomAttribute:
	
	def __init__(self):
		print("init")
		self.data = dict()

	def __getattr__(self, prop_name):
		print("get attribute %s " % (prop_name))
		return self.data[prop_name]

	# def __setattr__(self, prop_name, prop_value):
	#	self.data[prop_name] = prop_value

instance = CustomAttribute()

# instance["p1"] = "new value"
# print(instance["p1"])
# print(instance["c2"])