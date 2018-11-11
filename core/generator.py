print("example of inline generator")
inline_generator = (str(each) for each in range(1,5))
for i in inline_generator:
	print(i)

print("example of generator with 'yield'")
def my_generator(limit):
	values = range(1, limit+5)
	for x in values:
		if x%2==0:
			yield x
for i in my_generator(10):
	print(i)