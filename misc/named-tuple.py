from collections import namedtuple

CustomComputer = namedtuple("Computer", ["keyboard", "mouse", "monitor"])
my_computer = CustomComputer("Apple", "Logitech", ["Dell", "Dell", "NEC", "Built-in"])

# pay attention, namedtuple - CustomComputer, but class - Computer
print(my_computer) # Computer(keyboard='Apple', mouse='Logitech', monitor=['Dell', 'Dell', 'NEC', 'Built-in'])
# unpack parameters
print(*my_computer)    # Apple Logitech ['Dell', 'Dell', 'NEC', 'Built-in']
(my_keyboard, my_mouse, my_monitor) = my_computer
print(my_keyboard, my_mouse, my_monitor) # Apple Logitech ['Dell', 'Dell', 'NEC', 'Built-in']
# print fields by index
print(my_computer[0])  # Apple
print(my_computer[1])  # Logitech
print(my_computer[2])  # ["Dell", "Dell", "NEC", "Built-in"]
# print fields by name 
print(my_computer.keyboard) # Apple
print(my_computer.mouse)    # Logitech
print(my_computer.monitor)  # ["Dell", "Dell", "NEC", "Built-in"]


# extension
CustomNotebook = namedtuple("Notebook", CustomComputer._fields + ('battery', ))
print(CustomNotebook)
