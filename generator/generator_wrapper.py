class DataApiProxy(object):
    def __init__(self):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        # raise StopIteration()
        return 1
