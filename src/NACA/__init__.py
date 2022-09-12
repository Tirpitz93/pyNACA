from math import floor, sin, tan

import numpy as np
from numpy import pi, zeros, linspace, cos
from pandas import DataFrame, Series


class NACA(object):
    def __init__(self, identifier: [int, str], n: int = 100):
        self.identifier = identifier
        self.n = n
        if isinstance(identifier, int):
            self.m = identifier // 1000
            self.p = (identifier % 1000) // 100
            self.thickness = identifier % 100
        elif isinstance(identifier, str):
            self.m = int(identifier[0]) / 100
            self.p = int(identifier[1]) / 10
            self.thickness = int(identifier[2:]) / 100

        self.x = linspace(0, 1, n)
        self.top = zeros(n)
        self.bottom = zeros(n)



    def dat_file(self):
        df = DataFrame({"x": self.x+reversed(self.x), "y": self.top+reversed(self.bottom)})
        return  df.to_csv(sep="\t", index=False)
def cosine_spacing(s: np.array):
    """
    Generates a cosine spacing for the camber line.
    :param s:
    :return:
    """
    return 0.5 * (1 - cos(s * pi))


def four_digit(n: [str, int], alpha=0, c=1, s=100, cs: bool = False):
    """
    Generates a NACA 4-digit airfoil.
    :param n:
    :param alpha:
    :param c:
    :param s:
    :return: DataFrame
    """
    # 4 Digit Series
    x = linspace(0, 1, s + 1)
    if isinstance(n, str):
        thickness = int(n[2:]) / 100
    else:
        thickness = n % 100 / 100
    if cs:
        x = cosine_spacing(x)
    top_surface = 5 * thickness * (0.2969 * x ** 0.5 - 0.1260 * x - 0.3516 * x ** 2 + 0.2843 * x ** 3 - 0.1015 * x ** 4)
    bottom_surface = -top_surface
    # print(top_surface)
    # print(bottom_surface)
    return DataFrame({"x":x,'top': top_surface, 'bottom': bottom_surface})


if __name__ == '__main__':
    print(four_digit("0012", cs=True))


