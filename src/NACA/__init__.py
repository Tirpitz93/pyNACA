import re

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from numpy import arctan as atan, sin, cos, pi, zeros, linspace
from pandas import DataFrame, Series


class NACA(object):
    _subclasses: list["NACA"] = []

    def __init_subclass__(cls):
        NACA._subclasses.append(cls)

    def __init__(self, n: [str, int], alpha=0, chord_length=1, s=100, cs: bool = False):

        self.n = n
        self.alpha = alpha
        self.chord_length = chord_length
        self.s = s
        self.cs = cs
        self.xu = linspace(0, 1, s+1)
        self.xl = linspace(0, 1, s+1)
        self.yu = zeros(s+1)
        self.yl = zeros(s+1)
        self.df = DataFrame()
    def check_code(self, code):
        raise NotImplementedError

    # def dat_file(self):
    #     df = DataFrame({"x": np.concatenate(self.xu, self.xu), "y": np.concatenate(self.yu, self.yl)})
    #     return df.to_csv(sep="\t", index=False)

    def cosine_spacing(self, s: np.array):
        """
        Generates a cosine spacing for the camber line.
        :param s:
        :return:
        """
        return 0.5 * (1 - cos(s * pi))

    @classmethod
    def factory(cls, n: [str, int], alpha=0, c=1, s=100, cs: bool = False):
        for subclass in cls._subclasses:
            if subclass.check_code(n):
                return subclass(n, alpha, c, s, cs)
        else:
            raise ValueError("Invalid NACA code.")
    def plot(self) -> None:
        """
        Plots the airfoil.
        :return: None
        """

        fig, ax = plt.subplots()
        ax.plot(self.df["xu"], self.df["yu"])
        ax.plot(self.df["xl"], self.df["yl"])
        if "xc" in self.df.columns.tolist() and "yc" in self.df.columns.tolist():
            ax.plot(self.df["xc"], self.df["yc"])
        fig.legend(["Upper Surface", "Lower Surface", "Camber Line"])
        # plt.xlim(0, 1)
        # plt.ylim(-0.5, 0.5)
        plt.gca().set_aspect('equal', adjustable='box')
        fig.show()

class FourDigit(NACA):

    def __init__(self, n: [str, int], alpha=0, chord_length=1, s=100, cs: bool = True):
        """
        Generates a NACA 4-digit airfoil.
        :param n:
        :param alpha:
        :param chord_length:
        :param s:
        :return: DataFrame
        """
        super().__init__(n, alpha, chord_length, s, cs)
        # 4 Digit Series

        if isinstance(n, str):
            thickness = int(n[2:]) / 100
            camber = int(n[0]) / 100
            camber_position = int(n[1]) / 10
        else:
            thickness = n % 100 / 100
            camber = n // 1000 / 100
            camber_position = (n % 1000) // 100 / 10
        self.initial_x = linspace(0, 1, s + 1)
        if cs:
            self.initial_x = self.cosine_spacing(self.initial_x)
        # Camber Line
        self.initial_x * self.chord_length
        self.camber_gradient =  zeros(s + 1)
        self.y_camber = zeros(s + 1)
        if camber != 0:
            for i in range(s + 1):
                if self.initial_x[i] <= camber_position:
                    self.y_camber[i] = camber / camber_position ** 2 * (2 * camber_position * self.initial_x[i] - self.initial_x[i] ** 2)
                    self.camber_gradient[i] = 2 * camber / camber_position ** 2 * (camber_position - self.initial_x[i])
                else:
                    self.y_camber[i] = camber / (1 - camber_position) ** 2 * (
                            (1 - 2 * camber_position) + 2 * camber_position * self.initial_x[i] - self.initial_x[i] ** 2)
                    self.camber_gradient[i] = 2 * camber / (1 - camber_position) ** 2 * (camber_position - self.initial_x[i])

        self.initial_top = 5 * thickness * (0.2969 * self.initial_x ** 0.5 - 0.1260 * self.initial_x - 0.3516 * self.initial_x ** 2 + 0.2843 * self.initial_x ** 3 - 0.1015 * self.initial_x ** 4)
        # print(yu)
        # print(yl)
        self.x_lower = self.initial_x - self.initial_top * sin(atan(self.camber_gradient))
        self.x_upper = self.initial_x + self.initial_top * sin(atan(self.camber_gradient))
        self.y_lower = self.y_camber - self.initial_top * cos(atan(self.camber_gradient))
        self.y_upper = self.y_camber + self.initial_top * cos(atan(self.camber_gradient))
        self.df = DataFrame({"xu": self.x_upper, 'yu': self.y_upper, 'xl': self.x_lower, 'yl': self.y_lower, 'xc': self.initial_x, 'yc': self.y_camber})

        self.plot()



    @classmethod
    def check_code(cls, code):
        return (isinstance(code, int) and 1000 <= code <= 9000) or (isinstance(code, str) and re.match(r"^\d{4}$",
                                                                                                       code))


if __name__ == '__main__':
    NACA0012 = NACA.factory("2412", cs=True)
    # print(NACA0012.dat_file())
    print(NACA0012.df)
    NACA0012.plot()
