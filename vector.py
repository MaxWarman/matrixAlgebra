'''
    File name: vector.py
    Author: Maksymilian Górski
    Date created: 10/11/2020
    Date last modified: 10/11/2020
    Python Version: 3.6
    Purpose: Interpreting and calculating operations on n-dimensional Cartesian Vectors
'''

__all__ = ['Vector']
__author__ = "Maks Górski"
__license__ = "Public domain"
__email__ = "maksymilian_gorski@wp.pl"

import math


class Vector:

    def __init__(self, values):
        self.values = values
        self.dimension = len(values)

    def __str__(self):
        return f"{self.dimension}-dimensional Vector {self.values}"

    def __getitem__(self, index):
        return self.values[index]

    def __len__(self):
        return len(self.values)

    def __add__(self, vec2):
        return Vector([self.values[i] + vec2.values[i] for i in range(len(self))])

    def __sub__(self, vec2):
        return Vector([self.values[i] - vec2.values[i] for i in range(len(self))])

    def __abs__(self):
        sum = 0
        for i in range(len(self)):
            sum += self.values[i] ** 2
        return math.sqrt(sum)

    def __mul__(self, scalar):
        return Vector([self.values[i] * scalar for i in range(len(self))])

    __rmul__ = __mul__

    def __eq__(self, vec2):
        for i in range(len(self)):
            if self.values[i] != vec2.values[i]:
                return False
        return True

    def __matmul__(self, vec2):
        sum = 0
        for i in range(len(self)):
            sum += self.values[i] * vec2.values[i]
        return sum

    def __neg__(self):
        return self * (-1)


# Asserts

if __debug__ and __name__ == '__main__':
    assert Vector([1, 0, 2]) + Vector([0, 1, 2]) == Vector([1, 1, 4])
    assert Vector([5, 0, 3]) - Vector([4, 0, 2]) == Vector([1, 0, 1])
    assert Vector([1, 2, 3]) * 10 == Vector([10, 20, 30])
    assert 10 * Vector([1, 2, 3]) == Vector([10, 20, 30])
    assert Vector([2, 3, 4]) @ Vector([4, 3, 2]) == 25
    assert -Vector([2, 3, 4]) == Vector([-2, -3, -4])

print(Vector([1, 0, 2]) + Vector([0, 1, 2]))