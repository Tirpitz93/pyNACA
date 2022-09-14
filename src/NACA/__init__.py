import abc
import re
from functools import wraps

import numpy as np
from matplotlib import pyplot as plt
from numpy import arctan as atan, sin, sqrt
import pandas as pd
from numpy import cos, pi, zeros, linspace
from pandas import DataFrame, Series


def scale(func):
    """
    Decorator to scale the output of a function but the chord length
    :param func:
    :return:
    """

    @wraps(func)
    def scaled(self: "NACA", *args, **kwargs):
        print(f"Scaling by {self.chord_length}")
        print(self.__dict__)
        return func(self, *args, **kwargs) * self.chord_length

    scaled.__name__ = func.__name__
    scaled.__doc__ = func.__doc__
    return scaled


def round(func):
    """
    round
    :param func:
    :return:
    """

    @wraps(func)
    def scaled(self: "NACA", *args, **kwargs):
        print(f"Rounding to {self.precision}")
        print(self.__dict__)
        _ret = func(self, *args, **kwargs)
        return _ret.round(self.precision) if self.precision else _ret

    scaled.__name__ = func.__name__
    scaled.__doc__ = func.__doc__
    return scaled


class NACA(abc.ABC):
    """
    """

    subclasses = []

    def __init__(self, n: [str, int], alpha=0, chord_length=1, s=100, cs: bool = False, ct: bool = True, precision=0):
        raise NotImplementedError("Please Use NACA.factory() instead")
        self.n: str = str(n)
        self.alpha: float = alpha
        self.chord_length: float = chord_length
        self.s: int = s
        self.cs: bool = cs
        self.ct: bool = ct
        self.precision = precision

    def _base_init(self, n: [str, int], alpha=0, chord_length=1, s=100, cs: bool = False, ct: bool = True,
                   precision=0):
        pass

    def dat_file(self):
        df = DataFrame({"x": np.concatenate(self.xu, self.xu), "y": np.concatenate(self.yu, self.yl)})
        return df.to_csv(sep="\t", index=False)

    # def dat_file(self):
    #     df = DataFrame({"x": np.concatenate(self.xu, self.xu), "y": np.concatenate(self.yu, self.yl)})
    #     return df.to_csv(sep="\t", index=False)

    @classmethod
    def check_digits(cls, digits: [str, int]):
        return False

    @staticmethod
    def cosine_spacing(s: np.array):
        """
        Generates a cosine spacing for the camber line.
        :param s:
        :return:
        """
        return 0.5 * (1 - cos(s * pi))

    @classmethod
    def __init_subclass__(cls, **kwargs):
        print("init_subclass")
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)

    @property
    @scale
    def y_camber_line(self) -> DataFrame:
        raise NotImplementedError

    @property
    @scale
    def xu(self) -> DataFrame:
        raise NotImplementedError

    @property
    def x(self) -> Series:
        """
        Returns the x coordinates of the chord line.
        :return:
        """
        # print(self.s)
        x = linspace(0, 1, self.s + 1)
        series = Series(x if not self.cs else self.cosine_spacing(x), name="x")
        # fig, ax = plt.subplots()
        # ax.plot(series, marker="o")
        # fig.show()
        # print(series)
        return series

    @classmethod
    def factory(cls, n: [str, int], s=100, alpha=0, chord_length=1, cs: bool = False, precision=0):
        subclass: type(NACA)
        for subclass in cls.subclasses:
            if subclass.check_digits(n):
                return subclass(n=n, s=s, alpha=alpha, chord_length=chord_length, cs=cs, precision=precision)
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
        plt.title(f"NACA {self.n} {'cs' if self.cs else ''} Airfoil (Generated)")
        # plt.xlim(0, 1)
        # plt.ylim(-0.5, 0.5)
        plt.gca().set_aspect('equal', adjustable='box')
        fig.show()

    def plot_series(self, series: Series, **kwargs):
        fig, ax = plt.subplots()
        ax.plot(series, **kwargs)
        plt.gca().set_aspect('equal', adjustable='box')
        fig.show()

    @property
    def camber_line(self):
        """
        Returns the camber line.
        :return:
        """
        series = Series([self._camber_line(x) for x in self.x], name="Camber Line")
        # print(series)
        # self.plot_series(series)
        return series

    @property
    def camber_gradient(self):
        """
        Returns the camber gradient.
        :return:
        """

        series = Series([self._camber_gradient(x) for x in self.x], name="dycdx")
        # self.plot_series(series)
        return series

    @property
    def theta(self):
        theta = self._theta(self.camber_gradient)
        theta.rename("Theta", inplace=True)
        # print(theta)
        return theta

    @property
    @scale
    def yu(self) -> DataFrame:
        raise NotImplementedError

    @property
    @scale
    def xl(self) -> DataFrame:
        raise NotImplementedError

    @property
    @scale
    def yl(self) -> DataFrame:
        raise NotImplementedError

    @property
    def camber(self) -> DataFrame:
        return pd.concat([Series(self.x, name="xc"), self.y_camber_line, self.camber_gradient], axis=1, names=["xc", "yc", "dycdx"])

    @property
    def upper(self) -> DataFrame:
        upper = pd.concat([self.xu, self.yu], axis=1, names=["xu", "yu"])
        # print(upper)
        return upper

    @property
    def lower(self) -> DataFrame:
        lower = pd.concat([self.xl, self.yl], axis=1, names=["xl", "yl"])
        # print(lower)
        return lower

    @property
    @round
    def df(self) -> DataFrame:
        df = pd.concat([self.upper, self.lower, self.camber], axis=1, names=[["xu", "yu"], ["xl", "yl"],["xc","yc", "dycdx"]], )
        df.name = f"Airfoil: NACA {self.n}"
        return df

    def _camber_gradient(self, x):
        raise NotImplementedError

    def _camber_line(self, x):
        raise NotImplementedError

    def _theta(self, camber_gradient):
        return atan(camber_gradient)


class NACA4Digit(NACA):
    a1 = 0.2969
    a2 = -0.126
    a3 = -0.3516
    a4 = 0.2843
    a5 = -0.1015

    def __init__(self, n: [int, str], s: int = 100, alpha: float = 0, chord_length=1, cs: bool = False, ct: bool = True,
                 precision=0):
        self.n = n
        if isinstance(n, int):
            self.n = str(n)
        self.s = s
        print(f"n: {self.n}")
        print(f"s: {self.s}")
        self.cs = cs
        self.alpha = alpha
        self.chord_length = chord_length
        self.digit_1 = int(self.n[0])
        self.digit_2 = int(self.n[1])
        self.digit_3_4 = int(self.n[2:])
        self.thickness = self.digit_3_4 / 100

        self.max_camber = self.digit_1 / 100
        self.max_camber_position = self.digit_2 / 10
        self.ct = ct
        self.precision = precision
        print(self.ct)
        self.a5 = -0.1036 if self.ct else -0.1015
        print(self.a5)
        if self.ct:
            assert self.a5 == -0.1036
        else:
            assert self.a5 == -0.1015

    @property
    def y_camber_line(self) -> Series:
        series = Series([self._camber_line(x) for x in self.x], name="yc")
        # self.plot_series(series)
        return series

    def _camber_line(self, x):
        """
        Returns the y coordinate of the camber line at x.
        :param x:
        :return:
        """
        return self.max_camber / (self.max_camber_position ** 2) * (
                2 * self.max_camber_position * x - x ** 2) if x < self.max_camber_position else self.max_camber / (
                1 - self.max_camber_position) ** 2 * (
                1 - 2 * self.max_camber_position + 2 * self.max_camber_position * x - x ** 2)

    def _camber_gradient(self, x):
        """
        Returns the camber gradient at x.
        :param x:
        :return:
        """
        if x < self.max_camber_position:
            return 2 * self.max_camber / self.max_camber_position ** 2 * (self.max_camber_position - x)
        else:
            return 2 * self.max_camber / (1 - self.max_camber_position) ** 2 * (self.max_camber_position - x)

    def _thickness(self, x):
        """
        Returns the thickness of the airfoil.
        :return:
        """
        return self.thickness / 0.2 * (
                self.a1 * sqrt(x) + self.a2 * x + self.a3 * x ** 2 + self.a4 * x ** 3 + self.a5 * x ** 4)

    @property
    def y_thickness(self) -> Series:
        """
        Returns the y coordinates of the thickness.
        :return:
        """
        return Series([self._thickness(x) for x in self.x], name="Thickness")

    @classmethod
    def check_digits(cls, digits: [str, int]):
        if isinstance(digits, str):
            return True if re.match(r"^[\d]{4}$", digits) else False
        elif isinstance(digits, int):
            return True if 1000 <= digits <= 9999 else False
        raise TypeError("digits must be str or int")

    @property
    @scale
    def xu(self) -> Series:
        series = Series(self.x - self.y_thickness * sin(self.theta), name="xu")
        return series

    @property
    @scale
    def yu(self) -> Series:
        return Series(self.camber_line + self.y_thickness * cos(self.theta), name="yu")

    @property
    def xl(self) -> Series:
        return Series(self.x + self.y_thickness * sin(self.theta), name="xl")

    @property
    def yl(self) -> Series:
        return Series(self.camber_line - self.y_thickness * cos(self.theta), name="yl")


class NACA5DigitStandard(NACA4Digit):
    r_values = {
        1: 0.0580,
        2: 0.1260,
        3: 0.2025,
        4: 0.2900,
        5: 0.3910,

    }
    k_1_values = {
        1: 361.400,
        2: 51.640,
        3: 15.957,
        4: 6.643,
        5: 3.230,

    }

    def __init__(self, n: [int, str], s: int = 100, alpha: float = 0, chord_length=1, cs: bool = False, ct: bool = True,
                 precision=0):
        super().__init__(n=n, s=s, alpha=alpha, chord_length=chord_length, cs=cs, precision=precision)
        self.ct = ct
        self.precision = precision
        self.identifier = n
        if isinstance(n, int):
            self.identifier = str(n)
        self.n = s
        self.cs = cs
        self.chord_length = chord_length
        self.digit_1 = int(self.identifier[0])
        self.digit_2 = int(self.identifier[1])
        self.digit_3 = int(self.identifier[2])
        self.digit_4_5 = int(self.identifier[3:])

        self.max_camber = self.digit_1 / 10
        self.max_camber_position = self.digit_2 / 20

        self.design_cl = self.digit_1 * (3 / 20)

        self.thickness = self.digit_4_5 / 100
        self.reflex = False
        assert 0 <= self.max_camber <= 1
        assert 0.05 <= self.max_camber_position <= 0.5
        assert 0 <= self.thickness <= 1
        assert self.reflex is False

    def _camber_line(self, x):
        k1 = self.k_1_values[self.digit_2]
        r = self.r_values[self.digit_2]
        return (k1 / 6) * (x ** 3 - 3 * r * x ** 2 + r ** 2 * (3 - r) * x) if x <= self.max_camber_position else \
            ((k1 * r ** 3) / 6) * (1 - x)

    def _camber_gradient(self, x):
        k1 = self.k_1_values[self.digit_2]
        r = self.r_values[self.digit_2]
        return (k1 / 6) * (3 * x ** 2 - 6 * r * x + r ** 2 * (3 - r)) if x <= self.max_camber_position else \
            -((k1 * r ** 3) / 6)

    @classmethod
    def check_digits(cls, digits: [str, int]):
        if isinstance(digits, str):
            return True if re.match(r"^[\d]{2}0[\d]{2}$", digits) else False
        elif isinstance(digits, int):
            return True if 10000 <= digits <= 99999 and digits % 1000 // 100 == 0 else False
        raise TypeError("digits must be str or int")

    @classmethod
    def check_code(cls, code):
        return (isinstance(code, int) and 1000 <= code <= 9000) or (isinstance(code, str) and re.match(r"^\d{4}$",
                                                                                                       code))


class NACA5DigitReflex(NACA5DigitStandard):
    r_values = {
        2: 0.1300,
        3: 0.2170,
        4: 0.3180,
        5: 0.4410,
    }
    k_1_values = {
        2: 51.990,
        3: 15.793,
        4: 6.520,
        5: 3.191,
    }
    k_2_k_1_values = {
        2: 0.000764,
        3: 0.00677,
        4: 0.0303,
        5: 0.1355,
    }

    def __init__(self, n: [int, str], s: int = 100, alpha: float = 0, chord_length=1, cs: bool = False, ct: bool = True,
                 precision=0):

        super().__init__(n=n, s=s, alpha=alpha, chord_length=chord_length, cs=cs, precision=precision)
        self.reflex = True

    @classmethod
    def check_digits(cls, digits: [str, int]):
        if isinstance(digits, str):
            return True if re.match(r"^[\d]{2}1[\d]{2}$", digits) else False
        elif isinstance(digits, int):
            return True if 10000 <= digits <= 99999 and digits % 1000 // 100 == 1 else False
        raise TypeError("digits must be str or int")

    def _camber_line(self, x):
        r = self.r_values[self.digit_2]
        k1 = self.k_1_values[self.digit_2]
        k2_k1 = self.k_2_k_1_values[self.digit_2]
        return (
                (k1 / 6) *
                (
                        (x - r) ** 3
                        - (k2_k1 * (1 - r) ** 3) * x
                        - ((r ** 3) * x)
                        + r ** 3)
        ) \
            if x < self.max_camber_position else (
                (k1 / 6) *
                (
                        k2_k1 * (x - r) ** 3
                        - (k2_k1 * (1 - r) ** 3) * x
                        - ((r ** 3) * x)
                        + (r ** 3))
        )

    def _camber_gradient(self, x):
        r = self.r_values[self.digit_2]
        k1 = self.k_1_values[self.digit_2]
        k2_k1 = self.k_2_k_1_values[self.digit_2]
        return (
                (k1 / 6) *
                (
                        3 * (x - r) ** 2
                        - (k2_k1 * (1 - r) ** 3)
                        - (r ** 3))
        ) \
            if x < self.max_camber_position else (
                (k1 / 6) *
                (
                        3 * k2_k1 * (x - r) ** 2
                        - (k2_k1 * (1 - r) ** 3)
                        - (r ** 3))
        )


if __name__ == '__main__':
    ns = NACA.factory("23112", chord_length=4, cs=True)
    ni = NACA.factory(23112, chord_length=4, cs=True)
    print(ni.n)
    print(ni.__class__.__name__)

    NACA0012 = NACA.factory("2412", cs=True)
    # print(NACA0012.dat_file())
    print(NACA0012.__class__.__name__)
    NACA0012.plot()

    assert ns.n == ni.n
    assert ns.__class__.__name__ == ni.__class__.__name__
    assert ns.max_camber == ni.max_camber == 0.2
    assert ns.max_camber_position == ni.max_camber_position == 0.15
    assert ns.thickness == ni.thickness == 0.12
    print(ns.design_cl)
    assert ns.design_cl == ni.design_cl == 0.3
    print(ns.camber_line)
    print(ns.camber_gradient)
    n4s = NACA.factory("2312", chord=4)
    n4i = NACA.factory(2312, chord=4)
    print(n4s.n)
    print(n4s.__class__.__name__)
    assert n4s.n == n4i.n == "2312"
    assert n4s.__class__.__name__ == n4i.__class__.__name__ == "NACA4Digit"
    print(n4s.max_camber)
    assert n4s.max_camber == n4i.max_camber == 0.02
    assert n4s.max_camber_position == n4i.max_camber_position == 0.3
    assert n4s.thickness == n4i.thickness == 0.12
