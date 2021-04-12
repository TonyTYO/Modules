# -------------------------------------------------------------------------------
# Name:        rdict
# Purpose:     A dictionary class that also keeps a reverse dict
# Author:      Tony
# Created:     02/09/2020
# Copyright:   (c) Tony 2020
# Licence:     Free to use
# -------------------------------------------------------------------------------

# ! /usr/bin/env python

""" Implements dictionary with reverse look-up
    Dependencies : None
"""


class Rdict(dict):
    """ A dictionary that also stores its reverse """

    __slots__ = '_reverse'

    def __init__(self, mapping=None, **kwargs):
        super().__init__()

        self._reverse = {}
        self.update(mapping, **kwargs)

    @staticmethod
    def _process_args(mapping=None, **kwargs):
        """ Convert any parameters into list of tuples """
        if mapping is None:
            mapping = []
        if hasattr(mapping, 'items'):
            mapping = list(getattr(mapping, 'items')())
        return mapping + [t for t in getattr(kwargs, 'items')()]

    # ------------------------------------------------------------
    # Magic methods to re-implement dictionary methods

    def __setitem__(self, key, val):
        if key in self:
            del self[key]
        rev = self._reverse.get(val, None)
        if rev:
            if not isinstance(rev, list):
                rev = [rev]
            rev.append(key)
        else:
            rev = key
        self._reverse[val] = rev
        super().__setitem__(key, val)

    def __getitem__(self, key):
        return super().__getitem__(key)

    def __delitem__(self, key):
        val = super().pop(key)
        if val:
            self._delrev(key, val)

    def __repr__(self):
        return f"{type(self).__name__}({super().__repr__()})"

    def _delrev(self, key, val):
        rev = self._reverse.get(val, None)
        if isinstance(rev, list):
            rev.remove(key)
            self._reverse[val] = rev
        else:
            self._reverse.pop(val, None)

    # ------------------------------------------------------------
    # Overwritten methods

    def clear(self):
        self._reverse.clear()
        super().clear()

    def pop(self, *args):
        key = args[0]
        if len(args) > 1:
            val = super().pop(key, args[1])
            if val != args[1]:
                self._delrev(key, val)
        else:
            val = super().pop(key)
            self._delrev(key, val)
        return val

    def setdefault(self, *args):
        key, val = args[0], None
        if len(args) > 1:
            val = args[1]
        if key in self:
            return super().setdefault(key, val)
        else:
            self[key] = val
            return val

    def update(self, mapping=None, **kwargs):
        mapping = self._process_args(mapping, **kwargs)
        for tup in mapping:
            self.__setitem__(tup[0], tup[1])

    def fromkeys(self, keys, val=None):
        self._reverse[val] = list(keys)
        return super().fromkeys(keys, val)

    def popitem(self):
        key, val = super().popitem()
        self._delrev(key, val)
        return key, val

    # ------------------------------------------------------------
    # Additional methods to access reverse dictionary

    def rget(self, val, default=None):
        """ Reverse lookup - look up by value """
        return self._reverse.get(val, default)

    def ritems(self):
        """ Return all entries in reverse dict as tuples """
        return self._reverse.items()

    def rkeys(self):
        """ Return all keys in reverse dict """
        return self._reverse.keys()

    def rprint(self):
        """ Return printable form of reverse """
        return f"{type(self).__name__}.Reverse({self._reverse.__repr__()})"
