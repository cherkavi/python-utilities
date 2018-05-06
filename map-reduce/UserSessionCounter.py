from mrjob.job import MRJob

class UserSessionCounter(MRJob):

    def mapper(self, key, line):
        (id_visitor, id_session, *rest) = line.split("|")
        if len(id_visitor)==0 or id_visitor == 'id_visitor':
            return
        yield id_visitor, 1

    def reducer(self, id_visitor, occurences):
        yield id_visitor, sum(occurences)
