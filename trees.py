import copy


class TreeDB:
    """
    Class for DB tree:
        After creation you get default tree.
        It looks like:
            0: {'children': [2, 1], 'value': 'Node1'},
            1: {'children': [], 'value': 'Node2'},
            2: {'children': [4], 'value': 'Node3'},
            3: {'children': [], 'value': 'Node4'},
            4: {'children': [3, 5], 'value': 'Node5'},
            5: {'children': [], 'value': 'Node6'},

    Methods:
        apply(new_tree) - Apply changes from new_tree to DB tree
        reset() - Reset to instantly state
        get_element(number) - get whole(deep) copy of element with index "number"
        set_current(number) - set index "number" as a current element
        get_max() - get quantity elements in DB tree
    """

    def __init__(self):
        self.matrix = {
            # 0 - index:{
            # 'del':0 or 1 - index of deleting,
            # 'children': [2, 1] - 1 and 2 are indexes of children
            # 'value': 'Node1' - value in element}
            0: {'del': 0, 'children': [2, 1], 'value': 'Node1'},
            1: {'del': 0, 'children': [], 'value': 'Node2'},
            2: {'del': 0, 'children': [4], 'value': 'Node3'},
            3: {'del': 0, 'children': [], 'value': 'Node4'},
            4: {'del': 0, 'children': [3, 5], 'value': 'Node5'},
            5: {'del': 0, 'children': [], 'value': 'Node6'},
        }
        # Current marked element in tree
        self.current_item = None
        # Quantity of elements
        self.max = 5

    def apply(self, new_tree):
        """
            Apply changes from 'new_tree' to DB tree
        """
        # Special func for deleting children
        def del_children(item_list):
            # Check each children
            for i in item_list:
                # If it is in our new tree we will delete it below in main for
                if i not in new_tree:
                    # Mark element as deleted
                    self.matrix[i]['del'] = 1
                    # Call func again for current children
                    del_children(self.matrix[i]['children'])

        for key, value in new_tree.items():
            # We have to make whole copy of each element
            self.matrix[key] = {'del': value['del'], 'children': copy.deepcopy(value['children']),
                                'value': value['value']}
            # If there is 'del' mark, let's del children too
            if self.matrix[key]['del']:
                del_children(self.matrix[key]['children'])

    def reset(self):
        """
            Reset to instantly state
        """
        self.__init__()

    def get_element(self, number):
        """
            get whole(deep) copy of element with index "number"
        """
        return copy.deepcopy(self.matrix[number])

    def set_current(self, number):
        """
            set index "number" as a current element
        """
        self.current_item = number

    def get_max(self):
        """
            get quantity elements in DB tree
        """
        return self.max


class Tree:
    """
    Class for Cache tree:

    Methods:
        reset() - Reset to instantly state
        set_current(number) - set index "number" as a current element
        insert_element(element, number) - insert element "element" in tree as a child of element with index "number"
        add_element(element, number) - add new
        is_current_deleted() -  Check that current element is deleted or not
        del_element() - Delete element and all children
        set_value(value) - Set value for current element
        inc_max() - Increase quantity of elements
    """

    def __init__(self, my_max):
        self.matrix = {}
        self.current_item = None
        self.roots = []
        self.max = my_max

    def reset(self, my_max):
        """
            Reset to instantly state
        """
        self.__init__(my_max)

    def set_current(self, number):
        """
            set index "number" as a current element
        """
        self.current_item = number

    def insert_element(self, element, number):
        """
            insert element "element" in tree as a child of element with index "number"
            In these case we mean element from DB tree
        """
        # insert new element
        self.matrix[number] = element
        # We have to check if there are parent of element in our tree or not
        parent = list(filter(lambda x: number in self.matrix[x]['children'], self.matrix))
        if parent:
            # if there is we will mark it as a usual element
            self.matrix[number]['root'] = 0
            # if parent make as a deleted let's mark new too
            if self.matrix[parent[0]]['del']:
                self.matrix[number]['del'] = 1
            # If parent element has children which aren't in cache tree we will add special mark
            # self.matrix[parent[0]]['has_child'] = False
            # for el in self.matrix[parent[0]]['children']:
            #     if el not in self.matrix:
            #         self.matrix[parent[0]]['has_child'] = True
        else:
            # if not We will add index of element to list of roots and mark it as a root
            if number not in self.roots:
                self.roots.append(number)
            self.matrix[number]['root'] = 1

        # for each children of our new element we will have to check it in roots list. If there is let's del it
        # and mark as a usual element
        for el in self.matrix[number]['children']:
            if el in self.roots:
                self.roots.remove(el)
                self.matrix[el]['root'] = 0
            # If element has children which aren't in cache tree we will add special mark
            # if el not in self.matrix:
            #     self.matrix[number]['has_child'] = True

    def add_element(self, element, number):
        """
            insert element "element" in tree as a child of element with index "number"
            In these case we mean new element which doesn't exist in DB tree
        """
        # insert new element
        self.matrix[number] = element
        # Add new element in children of current
        self.matrix[self.current_item]['children'].append(number)

    def is_current_deleted(self):
        """
            Check that current element is deleted or not
        """
        if self.matrix[self.current_item]['del']:
            return True
        else:
            return False

    def del_element(self):
        """
            Delete element and all children
        """
        def del_all_children(item_list):
            # Iterate keys
            for i in item_list:
                # If key is int current cache tree we will mark it as a deleted
                if i in self.matrix:
                    self.matrix[i]['del'] = 1
                    # Call our function for children
                    del_all_children(self.matrix[i]['children'])

        if self.current_item is not None:
            del_all_children([self.current_item])

    def set_value(self, value):
        """
            Set value for current element
        """
        self.matrix[self.current_item]['value'] = value

    def inc_max(self):
        """
            Increase quantity of elements
        """
        self.max += 1
