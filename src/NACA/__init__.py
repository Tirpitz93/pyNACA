from math import floor, sin, cos, tan
from numpy import zeros, linspace
from pandas import DataFrame, Series
def four_digit(n: [str, int], alpha=0, c=1, s=100):
    """
    Generates a NACA 4-digit airfoil.
    :param n:
    :param alpha:
    :param c:
    :param s:
    :return: DataFrame
    """
    # 4 Digit Series
    x = linspace(0, 1, s+1)
    if isinstance(n, str):
        thickness = int(n[2:]) / 100
    else:
        thickness = n % 100 / 100

    top_surface = 5 * thickness* (0.2969 * x ** 0.5 - 0.1260 * x - 0.3516 * x ** 2 + 0.2843 * x ** 3 - 0.1015 * x ** 4)
    bottom_surface = -top_surface
    # print(top_surface)
    # print(bottom_surface)
    return DataFrame({ 'top': top_surface, 'bottom': bottom_surface}, index=Series(x,name="x"))



if __name__ == '__main__':
    print(four_digit("0012"))
