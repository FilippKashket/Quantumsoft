import copy

class TreeDB:
    def __init__(self):
        self.matrix = {
            0: {'del': 0, 'children': [2, 1], 'value': 'Node1'},
            1: {'del': 0, 'children': [], 'value': 'Node2'},
            2: {'del': 0, 'children': [4], 'value': 'Node3'},
            3: {'del': 0, 'children': [], 'value': 'Node4'},
            4: {'del': 0, 'children': [3, 5], 'value': 'Node5'},
            5: {'del': 0, 'children': [], 'value': 'Node6'},
        }
        self.current_item = None
        self.max = 5

    def apply(self, new_tree):
        for key in new_tree:
            self.matrix[key] = {'del': new_tree[key]['del'], 'children': new_tree[key]['children'],
                                'value': new_tree[key]['value']}

    def reset(self):
        self.__init__()

    def get_element(self, number):
        return copy.deepcopy(self.matrix[number])

    def set_current(self, number):
        self.current_item = number

    def get_max(self):
        return self.max


class Tree:
    def __init__(self, my_max):
        self.matrix = {}
        self.current_item = None
        self.roots = []
        self.max = my_max

    def reset(self, my_max):
        self.__init__(my_max)

    def set_current(self, number):
        self.current_item = number

    def insert_element(self, element, number):
        self.matrix[number] = element
        if list(filter(lambda x: number in self.matrix[x]['children'], self.matrix)):
            self.matrix[number]['root'] = 0
        else:
            self.roots.append(number)
            self.matrix[number]['root'] = 1

        for el in self.matrix[number]['children']:
            if el in self.matrix:
                self.roots.remove(el)
                self.matrix[el]['root'] = 0

    def add_element(self, element, number):
        self.matrix[number] = element
        self.matrix[self.current_item]['children'].append(number)

    def del_element(self):
        def del_all_children(item_list):
            for i in item_list:
                if i in self.matrix:
                    self.matrix[i]['del'] = 1
                    del_all_children(self.matrix[i]['children'])
        if self.current_item is not None:
            del_all_children([self.current_item])

    def set_value(self, value):
        self.matrix[self.current_item]['value'] = value

    def inc_max(self):
        self.max += 1

    def edit_element(self):
        return 'tree.edit'

    def copy_element(self, new_element):
        return new_element
