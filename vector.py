# -------------------------------------------------------------------------------
# Name:        vector
# Purpose:     Implements n_dimensional vectors
# Author:      Tony
# Created:     16/10/2020
# Copyright:   (c) Tony 2015
# Licence:     Free to use
# -------------------------------------------------------------------------------

# ! /usr/bin/env python

""" Implements n_dimensional vectors
    Dependencies : None
"""
from math import sqrt, sin, cos, atan, acos, degrees, copysign


class VectorError(Exception):
    """ Base class to handle errors """

    def __init__(self, message: str, where: str = "") -> None:
        message = f"Error {self.get_text(where)}: {message}"
        super().__init__(message)

    @staticmethod
    def get_text(where):
        return f"in {where}" if where else ""


class Vector(object):
    """ Class for 2-,3- ,4- or more vectors"""

    __slots__ = ['_vec', '_dim']

    def __init__(self, *args):
        """ Initialize vector and dimension
            args can be list, tuple or list of numbers
            can also give two points as tuples for vector between them
            If one component is float, convert all to float
        """
        if len(args) == 0:
            self._vec = []
        elif len(args) == 2 and isinstance(args[0], tuple) and isinstance(args[1], tuple):
            self._vec = [a - b for a, b in zip(args[1], args[0])]
        elif isinstance(args[0], list):
            self._vec = args[0]
        elif isinstance(args[0], tuple):
            self._vec = list(args[0])
        else:
            self._vec = list(args)

        if len(self._vec) < 2:
            self._vec.extend(0 for _ in range(2 - len(self._vec)))

        if any(isinstance(c, float) for c in self._vec):
            self._vec = [float(c) for c in self._vec]
        self._dim = len(self._vec)

    def set(self, *args):
        """ Set components to numbers given """
        if self._dim == 0:
            for arg in args:
                self._vec.append(arg)
        elif isinstance(args[0], tuple):
            for i in range(len(args[0])):
                self._vec[i] = args[0][i]
        elif len(args) <= self._dim:
            for i in range(len(args)):
                self._vec[i] = args[i]
        else:
            raise VectorError(f"No of values given exceeds vector dimension {self._dim}.", set.__name__)

    # --------------------------------------------------------
    # Getter and setter functions for vector, dim, x, y, z, t
    # x, y, z, t common notation for for 2-, 3-, and 4-vectors

    @property
    def vector(self):
        return self._vec

    @property
    def dim(self):
        return self._dim

    @property
    def x(self):
        return self._vec[0]

    @x.setter
    def x(self, val):
        self._vec[0] = val

    @property
    def y(self):
        return self._vec[1]

    @y.setter
    def y(self, val):
        self._vec[1] = val

    @property
    def z(self):
        if self._dim < 3:
            raise VectorError(f'Cannot return z-value. This is a {self._dim}-vector.', "")
        return self._vec[2]

    @z.setter
    def z(self, val):
        if self._dim > 2:
            self._vec[2] = val
        else:
            raise VectorError(f'Cannot set z-value. This is a {self._dim}-vector.', "")

    @property
    def t(self):
        if self._dim < 4:
            raise VectorError(f'Cannot return t-value. This is a {self._dim}-vector.', "")
        return self._vec[3]

    @t.setter
    def t(self, val):
        if self._dim > 3:
            self._vec[3] = val
        else:
            raise VectorError(f'Cannot set t-value. This is a {self._dim}-vector.', "")

    # --------------------------------------------------------
    # Getter and setter functions for length
    # Getter and setter functions for angle for 2-vectors

    @property
    def length(self):
        return self.get_length()

    @length.setter
    def length(self, value):
        lth = self.get_length()
        if lth != 0:
            mul = value / lth
            self._vec = [c * mul for c in self._vec]

    @property
    def angle(self):
        if self._dim == 2:
            return degrees(atan(self._vec[1] / self._vec[0]))
        return None

    @angle.setter
    def angle(self, value):
        if self._dim == 2:
            lth = self.get_length()
            self._vec = [lth * sin(value), lth * cos(value)]

    # --------------------------------------------------------
    # Magic Methods and Operator overloads

    # String representations
    def __str__(self):
        return f"{*self._vec,}"

    def __repr__(self):
        return f"Vector{*self._vec,}"

    # Magic methods to create a container class
    # Allows use of vector where list, tuple required
    def __len__(self):
        return len(self._vec)

    def __getitem__(self, key):
        if key < self._dim:
            return self._vec[key]
        else:
            raise VectorError(f'Cannot return value. This is a {self._dim}-vector.', "")

    def __setitem__(self, key, value):
        if key < self._dim:
            self._vec[key] = value
        else:
            raise VectorError(f'Cannot set value. This is a {self._dim}-vector.', "")

    def __iter__(self):
        return iter(self._vec[:])

    # Overloaded operators
    def __eq__(self, rhs):
        return rhs.dim == self._dim and all([a == b for a, b in zip(self._vec, rhs)])

    def __ne__(self, rhs):
        return rhs.dim != self._dim or any([a != b for a, b in zip(self._vec, rhs)])

    def __neg__(self):
        return Vector([-a for a in self._vec])

    def __add__(self, rhs):
        return Vector([a + b for a, b in zip(self._vec, rhs)])

    def __sub__(self, rhs):
        return Vector([a - b for a, b in zip(self._vec, rhs)])

    def __mul__(self, no):
        return Vector([c * no for c in self._vec])

    def __truediv__(self, no):
        return Vector([c / no for c in self._vec])

    def __radd__(self, rhs):
        return Vector([a + b for a, b in zip(self._vec, rhs)])

    def __rsub__(self, rhs):
        return Vector([a - b for a, b in zip(rhs, self._vec)])

    def __rmul__(self, no):
        return Vector([c * no for c in self._vec])

    def __iadd__(self, rhs):
        self._vec = [a + b for a, b in zip(self._vec, rhs)]
        return self

    def __isub__(self, rhs):
        self._vec = [a - b for a, b in zip(self._vec, rhs)]
        return self

    def __imul__(self, no):
        self._vec = [c * no for c in self._vec]
        return self

    def __itruediv__(self, no):
        self._vec = [c / no for c in self._vec]

    # --------------------------------------------------------
    # Vector functions

    def null(self):
        """ Return a new null vector """
        return Vector([0] * self._dim)

    def is_zero(self):
        """ Return True if all components 0 """
        return all(a == 0 for a in self._vec)

    def void(self):
        """ Set all components to 0 """
        self._vec = [0 for _ in self._vec]

    def get_length_sq(self):
        """ Return square of length """
        return sum([c ** 2 for c in self._vec])

    def get_length(self):
        """ Return length """
        return sqrt(self.get_length_sq())

    def normalise(self):
        """ Normalize vector """
        lth = self.get_length()
        if lth != 0:
            self._vec = [c / lth for c in self._vec]
        return self

    def get_normalised(self):
        """ Return new vector that is a normalized version of the vector """
        lth = self.get_length()
        if lth != 0:
            return Vector([c / lth for c in self._vec])
        else:
            return self.null()

    def truncate(self, max_length):
        """ Adjust  components so length does not exceed max_length """
        lth = self.get_length()
        if lth > max_length:
            self.length = max_length

    def tuple(self):
        """ Return vector as tuple """
        return tuple(self._vec)

    def dot(self, other):
        """ Return dot product with other """
        return sum([a * b for a, b in zip(self._vec, other.vector)])

    def cross(self, other):
        """ Return new vector that is cross product - for 3-vectors only """
        if self._dim == 3:
            return Vector([self._vec[2] * other[3] - self._vec[3] * other[2],
                           self._vec[3] * other[1] - self._vec[1] * other[3],
                           self._vec[1] * other[2] - self._vec[2] * other[1]])
        else:
            raise VectorError(f'Cross product only defined for 3-vectors. This is a {self._dim}-vector.', "")

    def get_angle(self, other):
        """ Return angle between vector and other """
        angle = acos(self.clip(self.dot(other) / (self.length * other.length), -1.0, +1.0))
        return degrees(angle)

    def distance(self, other):
        """ Return distance between vector and other """
        return (other - self).length

    def distance_sq(self, other):
        """ Return distance between vector and other """
        return (other - self).get_length_sq()

    def perpendicular(self):
        """ Return new unit vector perpendicular to vector """
        zeros = [idx for idx, val in enumerate(self._vec) if val == 0]
        if zeros:
            vec = self.null()
            vec[zeros[0]] = 1
        else:
            vec = self.null()
            vec[0] = -self.y
            vec[1] = self.x
        return vec.normalise()

    def reverse(self):
        """ Return new vector with signs reversed """
        return Vector([-c for c in self._vec])

    def reflect(self, norm):
        """ Return vector reflected in normalized vector norm """
        return self - norm * (2.0 * self.dot(norm))

    def direction(self, other):
        """ Return direction of other
            1 if clockwise, -1 if anticlockwise """
        return copysign(1, self.x * other.y - self.y * other.x)

    @staticmethod
    def clip(no, l_bound, u_bound):
        """ Limit no to range [l_bound, u_bound]
            used to avoid errors in math lib eg acos(1.0000000002)"""
        if no < l_bound:
            return l_bound
        elif no > u_bound:
            return u_bound
        else:
            return no
