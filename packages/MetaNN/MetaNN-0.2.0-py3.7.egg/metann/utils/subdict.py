import collections


class SubDict(collections.abc.MutableMapping):
    r"""
    Provide a sub dict **access** to a super dict.
    Parameters:
        :param super_dict (Mapping): The super dictionary where you want to take a sub dict
        :param keys (iterable): An iterable of keys according to which you want to access a sub dict
        :param keep_order (bool): If set to true the sub dict will keep the iteration order of the super dict
            when it is iterated. Default: True

    Examples::

        >>>super_dict = collections.OrderedDict({'a': 1, 'b': 2, 'c': 3})
        >>>sub_dict = SubDict(super_dict, keys=['a', 'b'])
    """
    def __init__(self, super_dict: collections.abc.Mapping, keys=[], keep_order=True):
        self.super_dict = super_dict
        self.sub_keys = set(keys)
        self.update_keys()
        self.keep_order = keep_order

    def __getitem__(self, item):
        if item in self.sub_keys:
            return self.super_dict.__getitem__(item)
        else:
            raise KeyError(item)

    def __setitem__(self, key, value):
        self.sub_keys.add(key)
        return self.super_dict.__setitem__(key, value)

    def __delitem__(self, key):
        self.sub_keys.remove(key)
        try:
            del self.super_dict[key]
        except KeyError:
            pass

    def __contains__(self, key):
        self.update_keys()
        return self.sub_keys.__contains__(key)

    def __iter__(self):
        if self.keep_order:
            for i in self.super_dict:
                if i in self.sub_keys:
                    yield i
        else:
            for i in self.sub_keys:
                yield i

    def __len__(self):
        self.update_keys()
        return len(self.sub_keys)

    def __str__(self):
        return "SubDict("+str(list(self))+")"

    def update_keys(self):
        r"""
        This method update the keys of the sub dict when the super dict is modified.

        .. note::

            **Do not** call this method when you use the built-in method only.

        :return:
        """
        self.sub_keys = self.sub_keys.intersection(self.super_dict.keys())