import abc
from abc import ABC

class Parent(ABC):

    @abc.abstractmethod
    def who_am_i(self):
        return "parent"


class Child(Parent):

    def who_am_i(self):
        return "child"

if __name__=="__main__":
    print(Child().who_am_i()) # child
    print( issubclass(Child, Parent) ) # True
    print( isinstance(Child(), Child) ) # True
    print( isinstance(Child(), Parent) ) # True
    print( isinstance(object(), Parent) ) # False
    # Parent() - can't create abstract class
