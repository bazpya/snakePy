class Tree(dict):
    def __init__(self, dictionary: dict):
        super(Tree, self).__init__(dictionary)
        for i, (key, val) in enumerate(dictionary.items()):
            if isinstance(val, dict):
                self[key] = Tree(val)
            else:
                self[key] = val

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Tree, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Tree, self).__delitem__(key)
        del self.__dict__[key]
