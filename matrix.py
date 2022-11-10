'''
    File name: matrix.py
    Author: Maksymilian Górski
    Date created: 10/11/2020
    Python Version: 3.6
    Purpose: Interpreting and calculating operations on n-dimensional Square Matrices
'''

__all__ = ['Matrix']
__author__ = "Maks Górski"
__license__ = "Public domain"
__email__ = "maksymilian_gorski@wp.pl"

import math

class Matrix:
    def __init__(self, values):
        if not math.sqrt(len(values)).is_integer():
            raise ValueError(
                f"The list provided must have length equal to square of natural number. Current length: {len(values)}")

        self.dimension = int(math.sqrt(len(values))), int(math.sqrt(len(values)))
        self.values = [[0 for i in range(self.dimension[0])] for j in range(self.dimension[1])]
        for i in range(self.dimension[0]):
            for j in range(self.dimension[1]):
                self.values[i][j] = values[i * self.dimension[0] + j]

    def __str__(self):
        return f"Columns:{self.dimension[0]}, Rows:{self.dimension[0]}, Indices:{self.dimension[0] ** 2} Values:{self.values}"

    def __getitem__(self, index):
        i, j = index
        return self.values[i][j]

    def __add__(self, m2):
        if self.dimension[0] != m2.dimension[0]:
            raise ValueError(
                f"The matrices must have the same lengths. Current lengths: {self.dimension[0] ** 2} & {m2.dimension[0] ** 2}")

        return self.__class__(
            [self[i, j] + m2[i, j] for i in range(self.dimension[0]) for j in range(self.dimension[1])])

    def __sub__(self, m2):
        if not self.dimension[0] == m2.dimension[0]:
            raise ValueError(
                f"The matrices must have the same lengths. Current lengths: {self.dimension[0] ** 2} & {len(m2.values) ** 2}")

        return self.__class__(
            [self[i, j] - m2[i, j] for i in range(self.dimension[0]) for j in range(self.dimension[1])])

    def __mul__(self, scalar):
        return self.__class__([self[i, j] * scalar for i in range(self.dimension[0]) for j in range(self.dimension[1])])

    __rmul__ = __mul__

    def __matmul__(self, other):

        try:
            if self.dimension[0] != other.dimension[0]:
                raise ValueError(
                    f"The matrices must have the same lengths. Current lengths: {self.dimension[0] ** 2} & {other.dimension[0] ** 2}")

            mul = [0 for i in range(self.dimension[0] ** 2)]
            for i in range(self.dimension[0]):
                for j in range(self.dimension[1]):
                    for k in range(self.dimension[0]):
                        mul[i * self.dimension[0] + j] += self[i, k] * other[k, j]

            return self.__class__(mul)

        except TypeError:
            if self.dimension[0] != other.dimension:
                raise ValueError(
                    f"The matrix and vector must have the same dimension. Current dim: {self.dimension} & {other.dimension}")

            trans = [0 for i in range(other.dimension)]
            for i in range(other.dimension):
                for j in range(other.dimension):
                    trans[i] += self[i, j] * other[j]
            return other.__class__(trans)

    def __eq__(self, m2):
        for i in range(self.dimension[0]):
            for j in range(self.dimension[1]):
                if self[i, j] != m2[i, j]:
                    return False
        return True

    def __neg__(self):
        return self * (-1)

    def det(self):
        det = 0
        mat = self

        if mat.dimension[0] == 1:
            return mat[0, 0]

        sign = 1

        for i in range(mat.dimension[0]):
            temp = Matrix.minor(mat, 0, i)
            
            print(f"{det} += {sign} * {mat[0,i]} * {temp.det()}")
            
            det += sign * mat[0, i] * temp.det()


            sign *= -1

        return det

    def minor(self, i, j):
        minor = []
        for x in range(self.dimension[0]):
            for y in range(self.dimension[1]):
                if x != i and y != j:
                    minor.append(self[x, y])
        return Matrix(minor)

    def transpose(self):
        m = self
        for i in range(m.dimension[0]):
            for j in range(m.dimension[1]):
                if i <= j:
                    continue
                buffer = m[i,j]
                m.values[i][j] = m[j,i]
                m.values[j][i] = buffer
        return m

    def invert(self):
        det = self.det()
        if det == 0:
            raise ValueError("The determinant of given matrix is 0, so it cannot be inverted.")

        n = Matrix([0 for i in range(self.dimension[0]**2)])
        sign = 1
        for i in range(n.dimension[0]):
            for j in range(n.dimension[1]):
                n.values[i][j] = self.minor(i,j).det() * sign
                sign = -sign
        n = n.transpose()
        inv = (1/det) * n
        return inv

    def near_zero(self, accuracy):
        for i in range(self.dimension[0]):
            for j in range(self.dimension[1]):
                if abs(self[i,j]) > accuracy:
                    return False
        return True

    @classmethod
    def unit(cls, dimension):
        m = [0 for i in range(dimension**2)]
        for i in range(dimension):
            for j in range(dimension):
                if i == j:
                    m[i*dimension + j] = 1
        return cls(m)


# Asserts
from vector import Vector

def main():
    m1 = Matrix([3,4,-1,-1])
    m2 = Matrix([1,2,3,4])

    print(m1)
    print(m2)
    print(m1.invert())

    print((m1@m2)@m1.invert())

def runAssertionTests():
    assert Matrix([1, 2, 3, 4]) + Matrix([2, 3, 4, 5]) == Matrix([3, 5, 7, 9])
    assert Matrix([1, 2, 3, 4]) - Matrix([2, 3, 4, 5]) == Matrix([-1, -1, -1, -1])
    assert Matrix([1, 2, 3, 4]) * 10 == Matrix([10, 20, 30, 40])
    assert 10 * Matrix([1, 2, 3, 4]) == Matrix([10, 20, 30, 40])
    assert -Matrix([1, 2, 3, 4]) == Matrix([-1, -2, -3, -4])
    assert Matrix([1, 2, 3, 4]) == Matrix([1, 2, 3, 4])
    assert Matrix.minor(Matrix([1, 2, 3, 4, 5, 6, 7, 8, 9]), 0, 0) == Matrix([5, 6, 8, 9])
    assert Matrix([4, 3, 2, 2, 0, 1, -3, 3, 0, -1, 3, 3, 0, 3, 1, 1]).det() == -240


    m1 = Matrix([1, 2, 3, 4])
    m2 = Matrix([5, 6, 7, 8])
    assert m1.det() * m2.det() == (m1 @ m2).det()

    m3 = Matrix([6, 8, 10, 12])
    for i in range(m1.dimension[0]):
        for j in range(m1.dimension[0]):
            assert m3[i, j] == m1[i, j] + m2[i, j]

    v1 = Vector([1, 2])
    assert (m1 @ m2) @ v1 == m1 @ (m2 @ v1)

    c = 13
    assert (c * m1).det() == c ** m1.dimension[0] * m1.det()

    m1 = Matrix([-1, 2, -3, 5, 8, -9, 4, 7, -7])
    m2 = Matrix([5, 6, 7, 8, 9, 10, -1, -2, 3])
    I = Matrix([1, 0, 0,   0, 1, 0,   0, 0, 1])
    assert (I + m1 @ m2).det() == (I + m2 @ m1).det()
    assert (m1 @ m1.invert() - Matrix.unit(m1.dimension[0])).near_zero(0.001)

if __debug__ and __name__ == '__main__':
    runAssertionTests()    
    main()

if __name__ == '__main__':
    main()