files_with_control_date = [each for each in source_list if each not in except_list]


class SubstractAbleList(list):
    def __init__(self, *args):
        super(SubstractAbleList, self).__init__(args)

    def __sub__(self, another_list):
        substracted_list = [each for each in self if each not in antoher_list]
        return self.__class__(*substracted_list)


