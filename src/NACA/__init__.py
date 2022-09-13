import abc
import re
from functools import wraps

import numpy as np
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


class NACA(abc.ABC):
    """

    """
    subclasses = []

    def __init__(self):
        """
        Do not call this directly. Use NACA.factory().
        """
        raise TypeError("Use NACA.factory() to create a NACA object")
        self.chord_length = 1
        self.n = 100
        self.cs = False
        self.thickness = 0.12

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
    def factory(cls, identifier: [int, str], n: int = 100, chord=1, cs: bool = False):
        for subclass in cls.subclasses:
            if subclass.check_digits(identifier):
                return subclass(identifier, n, chord, cs)
        raise ValueError(f"Invalid NACA identifier: {identifier}")

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
        return Series(linspace(0, 1, self.n + 1), name="x" ) if not self.cs else Series(self.cosine_spacing(linspace(0, 1, self.n + 1) ), name="x")

    @property
    @scale
    def spacing(self) -> np.array:
        """
        Returns the spacing of the camber line.
        :return:
        """
        return self.x

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
    def camber_gradient(self):
        """
        Returns the camber gradient.
        :return:
        """

        return Series([self._camber_gradient(x) for x in self.x], index=self.x, name="Camber Gradient")

    @property
    def camber_line(self):
        """
        Returns the camber line.
        :return:
        """
        return Series([self._camber_line(x) for x in self.x], index=self.x, name="Camber Line")


    @property
    def camber(self) -> DataFrame:
        return pd.concat([self.x, self.y_camber_line, self.camber_gradient], axis=1)

    @property
    def upper(self) -> DataFrame:
        return pd.concat([self.xu, self.yu], axis=1)

    @property
    def lower(self) -> DataFrame:
        return pd.concat([self.xl, self.yl], axis=1)

    @property
    def df(self):
        return pd.concat([self.upper, self.lower, self.camber], axis=1)

    def _camber_gradient(self, x):
        raise NotImplementedError

    def _camber_line(self, x):
        raise NotImplementedError


class NACA4Digit(NACA):
    a1 = 0.2969
    a2 = -0.126
    a3 = -0.3516
    a4 = 0.2843
    a5 = -0.1015
    def __init__(self, identifier: [int, str], n: int = 100, chord=1, cs: bool = False, ct:bool=False):
        self.identifier = identifier
        if isinstance(identifier, int):
            self.identifier = str(identifier)
        self.n = n
        self.chord_length = chord
        self.ct = ct
        if self.ct:
            self.a5 = 0.1036

        self.max_camber = int(self.identifier[0]) / 100
        self.max_camber_position = int(self.identifier[1]) / 10
        self.thickness = int(self.identifier[2:]) / 100
        self.top = zeros(n)
        self.bottom = zeros(n)
        self.cs = cs
        if self.ct:
            assert self.a5 == 0.1036
        else:
            assert self.a5 == -0.1015

    def _camber_line(self, x):
        """
        Returns the y coordinate of the camber line at x.
        :param x:
        :return:
        """
        if x < self.max_camber_position:
            return self.max_camber / self.max_camber_position ** 2 * (2 * self.max_camber_position * x - x ** 2)
        else:
            return self.max_camber / (1 - self.max_camber_position) ** 2 * (
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


    @classmethod
    def check_digits(cls, digits: [str, int]):
        if isinstance(digits, str):
            return True if re.match(r"^[\d]{4}$", digits) else False
        elif isinstance(digits, int):
            return True if 1000 <= digits <= 9999 else False
        raise TypeError("digits must be str or int")



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

    def __init__(self, identifier: [int, str], n: int = 100, chord=1, cs: bool = False):

        self.identifier = identifier
        if isinstance(identifier, int):
            self.identifier = str(identifier)
        self.n = n
        self.cs = cs
        self.chord_length = chord
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
        return (k1/6)*(x**3 - 3*r*x**2 + r**2*(3-r)*x) if x <= self.max_camber_position else \
            ((k1*r**3)/6)*(1-x)

    def _camber_gradient(self, x):
        k1 = self.k_1_values[self.digit_2]
        r = self.r_values[self.digit_2]
        return (k1/6)*(3*x**2 - 6*r*x + r**2*(3-r)) if x <= self.max_camber_position else \
            -((k1*r**3)/6)

    @classmethod
    def check_digits(cls, digits: [str, int]):
        if isinstance(digits, str):
            return True if re.match(r"^[\d]{2}0[\d]{2}$", digits) else False
        elif isinstance(digits, int):
            return True if 10000 <= digits <= 99999 and digits % 1000 // 100 == 0 else False
        raise TypeError("digits must be str or int")


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

    def __init__(self, identifier: [int, str], n: int = 100, chord=1, cs: bool = False):

        super().__init__(identifier, n, chord, cs)
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
    @property
    def camber_line(self):
        return Series([self._camber_line(x) for x in self.x], index=self.x)


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
    @property
    def camber_gradient(self):


        return Series([self._camber_gradient(x) for x in self.x], index=self.x)

if __name__ == '__main__':
    ns = NACA.factory("23112", chord=4, cs=True)
    ni = NACA.factory(23112, chord=4, cs=True)
    print(ni.identifier)
    print(ni.__class__.__name__)
    assert ns.identifier == ni.identifier
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
    print(n4s.identifier)
    print(n4s.__class__.__name__)
    assert n4s.identifier == n4i.identifier == "2312"
    assert n4s.__class__.__name__ == n4i.__class__.__name__ == "NACA4Digit"
    print(n4s.max_camber)
    assert n4s.max_camber == n4i.max_camber == 0.02
    assert n4s.max_camber_position == n4i.max_camber_position == 0.3
    assert n4s.thickness == n4i.thickness == 0.12