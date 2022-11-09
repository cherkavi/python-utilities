cls = type('my_class', (object,), {'__doc__': 'example of dynamically created class'})

print(cls)
print(cls.__doc__)
